using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text.RegularExpressions;
using System.Threading;
using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.AddressableAssets;
using UnityEngine.AddressableAssets.ResourceLocators;
using UnityEngine.ResourceManagement.ResourceLocations;
using UnityEngine.ResourceManagement.ResourceProviders;

public static class GotchiCustomRenderCLI
{
    private static IResourceLocator s_EditorWearableLocator;

    public static void RenderFromJson()
    {
        Directory.CreateDirectory(Path.Combine(Directory.GetCurrentDirectory(), "Renders"));
        var tracePath = Path.Combine(Directory.GetCurrentDirectory(), "Renders", "cli-trace.log");
        File.AppendAllText(tracePath, "entered RenderFromJson\n");

        var args = Environment.GetCommandLineArgs();
        var inputPath = GetArgValue(args, "--input");
        File.AppendAllText(tracePath, $"input={inputPath}\n");

        if (string.IsNullOrEmpty(inputPath) || !File.Exists(inputPath))
        {
            Fail(tracePath, "missing_input", "Expected --input <json-path> for custom gotchi render request.");
            return;
        }

        var request = JsonUtility.FromJson<GotchiRenderRequest>(File.ReadAllText(inputPath));
        if (request == null)
        {
            Fail(tracePath, "bad_input", "Could not parse render request JSON.");
            return;
        }

        EnsureParent(request.output.full_png);
        EnsureParent(request.output.headshot_png);
        EnsureParent(request.output.manifest_json);

        var holder = CreateRenderHolder(tracePath);
        if (holder == null)
        {
            Fail(tracePath, "holder_missing", "Could not locate or instantiate the SDK render holder prefab.");
            return;
        }

        try
        {
            ConfigureRenderLayer(tracePath, holder);

            var gotchiBase = holder.AavegotchiRenderer ?? holder.GetComponentInChildren<Aavegotchi_Base>(true);
            if (gotchiBase == null)
            {
                Fail(tracePath, "sdk_component_missing", "Aavegotchi_Base component was not found on the selected SDK render holder.");
                return;
            }

            InitializeSdkComponents(tracePath, gotchiBase);

            var data = BuildData(request);
            var wearablesReady = PrepareWearables(tracePath, gotchiBase, data);
            File.AppendAllText(tracePath, $"wearablesReady={wearablesReady}\n");

            var repairedMaterials = RepairMissingShaders(tracePath, gotchiBase.gameObject);
            File.AppendAllText(tracePath, $"repairedMaterials={repairedMaterials}\n");

            var fullBg = ParseBackground(request.background);
            var poseStyle = NormalizePose(request.pose);
            ApplyPose(tracePath, gotchiBase, poseStyle);
            ConfigureStudioLighting(tracePath, holder, fullBg);
            CaptureFullAndHeadshot(tracePath, holder, gotchiBase, request, poseStyle, fullBg);

            var result = new GotchiRenderResult
            {
                ok = true,
                status = wearablesReady ? "rendered" : "rendered_with_async_warning",
                message = wearablesReady
                    ? "Camera captures were written using the Unity SDK render holder."
                    : "Camera captures were written, but wearable loading did not confirm synchronously; inspect outputs for missing wearable assets.",
                full_png = request.output.full_png,
                headshot_png = request.output.headshot_png,
                manifest_json = request.output.manifest_json,
                unity_version = Application.unityVersion,
                request = request,
            };

            File.AppendAllText(tracePath, "writing manifest\n");
            var json = JsonUtility.ToJson(result, true);
            File.WriteAllText(request.output.manifest_json, json);
            Console.WriteLine(json);
        }
        finally
        {
            if (holder != null)
            {
                UnityEngine.Object.DestroyImmediate(holder.gameObject);
            }
            AssetDatabase.SaveAssets();
        }
    }

    private static AavegotchiRenderTextureHolder CreateRenderHolder(string tracePath)
    {
        string[] preferredNames = { "AavegotchiRenderTextureHolder" };
        foreach (var name in preferredNames)
        {
            var guids = AssetDatabase.FindAssets($"{name} t:Prefab");
            File.AppendAllText(tracePath, $"search={name} matches={guids.Length}\n");
            foreach (var guid in guids)
            {
                var path = AssetDatabase.GUIDToAssetPath(guid);
                File.AppendAllText(tracePath, $"candidate={path}\n");
                var prefab = AssetDatabase.LoadAssetAtPath<GameObject>(path);
                if (prefab == null) continue;
                var instance = PrefabUtility.InstantiatePrefab(prefab) as GameObject;
                if (instance == null) continue;
                var holder = instance.GetComponent<AavegotchiRenderTextureHolder>();
                if (holder != null)
                {
                    File.AppendAllText(tracePath, $"selected={path}\n");
                    return holder;
                }
                UnityEngine.Object.DestroyImmediate(instance);
            }
        }
        return null;
    }

    private static void ConfigureRenderLayer(string tracePath, AavegotchiRenderTextureHolder holder)
    {
        var renderLayer = FirstLayerFromMask(holder.RenderCamera.cullingMask);
        if (renderLayer < 0)
        {
            renderLayer = 7;
            holder.RenderCamera.cullingMask = 1 << renderLayer;
        }

        SetLayerRecursively(holder.gameObject, renderLayer);
        File.AppendAllText(tracePath, $"renderLayer={renderLayer} cullingMask={holder.RenderCamera.cullingMask}\n");
    }

    private static int FirstLayerFromMask(int mask)
    {
        for (var i = 0; i < 32; i++)
        {
            if ((mask & (1 << i)) != 0) return i;
        }

        return -1;
    }

    private static void SetLayerRecursively(GameObject obj, int layer)
    {
        obj.layer = layer;
        foreach (Transform child in obj.transform)
        {
            SetLayerRecursively(child.gameObject, layer);
        }
    }

    private static bool PrepareWearables(string tracePath, Aavegotchi_Base gotchiBase, Aavegotchi_Data data)
    {
        var locations = EnsureEditorWearableLocator(tracePath);
        File.AppendAllText(tracePath, $"wearableLocations={(locations == null ? 0 : locations.Count)}\n");

        var field = typeof(Aavegotchi_Base).GetField("WearableAssetList", BindingFlags.NonPublic | BindingFlags.Instance);
        field?.SetValue(gotchiBase, locations);

        foreach (var id in RequestedWearableIds(data))
        {
            var key = $"Wearable_Mesh_{id}";
            var location = locations?.FirstOrDefault(l => l.PrimaryKey == key);
            File.AppendAllText(tracePath, $"preload={key} found={(location != null)}\n");
            if (location != null)
            {
                Addressables.LoadAssetAsync<GameObject>(location).WaitForCompletion();
            }
        }

        var completed = false;
        gotchiBase.UpdateForData(data, () =>
        {
            completed = true;
            File.AppendAllText(tracePath, "UpdateForData callback\n");
        }, true);

        for (var i = 0; i < 20 && !completed; i++)
        {
            Thread.Sleep(50);
        }

        if (!completed)
        {
            File.AppendAllText(tracePath, "syncWearableFallback=1\n");
            completed = LoadWearablesSynchronously(tracePath, gotchiBase, data, locations);
            if (completed)
            {
                gotchiBase.gameObject.SetActive(true);
                InvokeGotchiUpdateWearableLinks(tracePath, gotchiBase);
            }
        }

        var requestedWearables = RequestedWearableIds(data).Count();
        var hasCatalog = locations != null && locations.Count > 0;
        return completed && (requestedWearables == 0 || hasCatalog);
    }

    private static IList<IResourceLocation> EnsureEditorWearableLocator(string tracePath)
    {
        Addressables.InitializeAsync().WaitForCompletion();
        EnsureAssetDatabaseProvider(tracePath);

        if (s_EditorWearableLocator != null)
        {
            Addressables.RemoveResourceLocator(s_EditorWearableLocator);
            s_EditorWearableLocator = null;
            File.AppendAllText(tracePath, "editorLocatorRemoved=1\n");
        }

        var locator = new ResourceLocationMap("GotchiCustomEditorLocator");
        var meshLocations = new List<IResourceLocation>();
        var wearableMeshCount = 0;
        var wearableMaterialCount = 0;
        var seenKeys = new HashSet<string>(StringComparer.Ordinal);
        var roots = new[]
        {
            "Packages/com.pixelcraft_studios.aavegotchi_unity_sdk/Runtime/AddressableAssets"
        };

        foreach (var guid in AssetDatabase.FindAssets("Wearable_Mesh_ t:Prefab", roots).OrderBy(g => g, StringComparer.Ordinal))
        {
            var path = AssetDatabase.GUIDToAssetPath(guid);
            var asset = AssetDatabase.LoadAssetAtPath<GameObject>(path);
            if (asset == null) continue;

            var key = asset.name;
            if (!seenKeys.Add($"mesh:{key}")) continue;

            var location = new ResourceLocationBase(key, path, typeof(AssetDatabaseProvider).FullName, typeof(GameObject));
            locator.Add(key, location);
            locator.Add("Wearable", location);
            meshLocations.Add(location);
            wearableMeshCount++;
        }

        foreach (var guid in AssetDatabase.FindAssets("Wearable_Mat_ t:Material", roots).OrderBy(g => g, StringComparer.Ordinal))
        {
            var path = AssetDatabase.GUIDToAssetPath(guid);
            var asset = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (asset == null) continue;

            var key = asset.name;
            if (!seenKeys.Add($"mat:{key}")) continue;

            locator.Add(key, new ResourceLocationBase(key, path, typeof(AssetDatabaseProvider).FullName, typeof(Material)));
            wearableMaterialCount++;
        }

        Addressables.AddResourceLocator(locator);
        s_EditorWearableLocator = locator;

        File.AppendAllText(tracePath, $"editorLocatorMeshes={wearableMeshCount}\n");
        File.AppendAllText(tracePath, $"editorLocatorMaterials={wearableMaterialCount}\n");

        return meshLocations;
    }

    private static void EnsureAssetDatabaseProvider(string tracePath)
    {
        var exists = Addressables.ResourceManager.ResourceProviders.Any(p => p.GetType() == typeof(AssetDatabaseProvider));
        if (exists)
        {
            File.AppendAllText(tracePath, "assetDatabaseProviderPresent=1\n");
            return;
        }

        Addressables.ResourceManager.ResourceProviders.Add(new AssetDatabaseProvider(-1f));
        File.AppendAllText(tracePath, "assetDatabaseProviderAdded=1\n");
    }

    private static bool LoadWearablesSynchronously(string tracePath, Aavegotchi_Base gotchiBase, Aavegotchi_Data data, IList<IResourceLocation> locations)
    {
        var loader = gotchiBase.Wearable_Loader;
        if (loader == null)
        {
            File.AppendAllText(tracePath, "syncLoaderMissing=1\n");
            return false;
        }

        loader.LoadedWearables.Clear();

        var allLoaded = true;
        var loadedCount = 0;

        foreach (var (slot, wearableId) in RequestedWearableSlots(data))
        {
            if (wearableId <= 0) continue;
            if (LoadWearableSynchronously(tracePath, loader, slot, wearableId, data.SkinID, locations))
            {
                loadedCount++;
            }
            else
            {
                allLoaded = false;
            }
        }

        File.AppendAllText(tracePath, $"syncLoadedCount={loadedCount}\n");
        return allLoaded;
    }

    private static bool LoadWearableSynchronously(string tracePath, Aavegotchi_WearableLoader loader, EWearableSlot slot, int wearableId, int skinId, IList<IResourceLocation> locations)
    {
        var key = skinId > 0 ? $"Wearable_Mesh_{wearableId}_{skinId}" : $"Wearable_Mesh_{wearableId}";
        var location = locations?.FirstOrDefault(l => l.PrimaryKey == key);
        if (location == null)
        {
            File.AppendAllText(tracePath, $"syncMissingLocation={key}\n");
            return false;
        }

        var prefab = Addressables.LoadAssetAsync<GameObject>(location).WaitForCompletion();
        if (prefab == null)
        {
            File.AppendAllText(tracePath, $"syncMissingPrefab={key}\n");
            return false;
        }

        var instance = UnityEngine.Object.Instantiate(prefab, loader.transform);
        var wearable = instance.GetComponent<Aavegotchi_Wearable>();
        if (wearable == null)
        {
            File.AppendAllText(tracePath, $"syncMissingWearableComponent={key}\n");
            UnityEngine.Object.DestroyImmediate(instance);
            return false;
        }

        SetLayerRecursively(instance, loader.gameObject.layer);
        wearable.EquippedSlot = slot;
        SynchronizeWearableBones(loader, wearable, slot);
        SynchronizeWearableAttachments(loader, wearable);
        SynchronizeWearableHandSlots(wearable, slot);
        AttachWearableToSlot(loader, wearable, slot);
        ApplyWearableMaterialSynchronously(tracePath, wearable);
        wearable.gameObject.SetActive(true);
        loader.LoadedWearables[slot] = wearable;
        File.AppendAllText(tracePath, $"syncLoaded={key} slot={slot}\n");
        return true;
    }

    private static void SynchronizeWearableBones(Aavegotchi_WearableLoader loader, Aavegotchi_Wearable wearable, EWearableSlot slot)
    {
        var mainBodyRenderer = GetPrivateField<SkinnedMeshRenderer>(loader, "MainBodyRenderer");
        var skinnedMeshRenderers = GetPrivateField<List<SkinnedMeshRenderer>>(wearable, "SkinnedMeshRenderers") ?? new List<SkinnedMeshRenderer>();
        foreach (var skinnedMeshRenderer in skinnedMeshRenderers)
        {
            if (skinnedMeshRenderer == null || mainBodyRenderer == null) continue;
            skinnedMeshRenderer.bones = mainBodyRenderer.bones;
            skinnedMeshRenderer.rootBone = loader.RootBone;
        }

        if (wearable.IsSkinnedWeapon && skinnedMeshRenderers.Count == 2)
        {
            skinnedMeshRenderers[0].gameObject.SetActive(slot == EWearableSlot.Hand_left);
            skinnedMeshRenderers[1].gameObject.SetActive(slot == EWearableSlot.Hand_right);
        }
    }

    private static void SynchronizeWearableAttachments(Aavegotchi_WearableLoader loader, Aavegotchi_Wearable wearable)
    {
        foreach (var toSpawn in wearable.Attachments)
        {
            foreach (var attachmentPoint in loader.AttachmentPoints)
            {
                if (attachmentPoint.Name != toSpawn.Name || attachmentPoint.Target == null || toSpawn.ToAttach == null) continue;
                var spawnedObj = UnityEngine.Object.Instantiate(toSpawn.ToAttach, attachmentPoint.Target);
                SetLayerRecursively(spawnedObj, attachmentPoint.Target.gameObject.layer);
                break;
            }
        }
    }

    private static void SynchronizeWearableHandSlots(Aavegotchi_Wearable wearable, EWearableSlot slot)
    {
        var meshRenderers = GetPrivateField<List<MeshRenderer>>(wearable, "MeshRenderers") ?? new List<MeshRenderer>();
        if (slot == EWearableSlot.Hand_left && wearable.LeftHandTransform != null)
        {
            foreach (var meshRenderer in meshRenderers)
            {
                if (meshRenderer != null) meshRenderer.transform.SetParent(wearable.LeftHandTransform, false);
            }
        }
        else if (slot == EWearableSlot.Hand_right && wearable.RightHandTransform != null)
        {
            foreach (var meshRenderer in meshRenderers)
            {
                if (meshRenderer != null) meshRenderer.transform.SetParent(wearable.RightHandTransform, false);
            }
        }
    }

    private static void ApplyWearableMaterialSynchronously(string tracePath, Aavegotchi_Wearable wearable)
    {
        var materialName = GetPrivateField<string>(wearable, "MaterialName");
        if (string.IsNullOrWhiteSpace(materialName))
        {
            File.AppendAllText(tracePath, $"syncMaterialSkipped={wearable.WearableID}\n");
            return;
        }

        var material = Addressables.LoadAssetAsync<Material>($"Wearable_Mat_{materialName}").WaitForCompletion();
        if (material == null)
        {
            File.AppendAllText(tracePath, $"syncMaterialMissing={materialName}\n");
            return;
        }

        var skinnedMeshRenderers = GetPrivateField<List<SkinnedMeshRenderer>>(wearable, "SkinnedMeshRenderers") ?? new List<SkinnedMeshRenderer>();
        foreach (var skinnedMeshRenderer in skinnedMeshRenderers)
        {
            if (skinnedMeshRenderer == null) continue;
            if (skinnedMeshRenderer.materials.Length > 1)
            {
                var materialsCopy = skinnedMeshRenderer.materials;
                for (var i = 0; i < materialsCopy.Length; ++i) materialsCopy[i] = material;
                skinnedMeshRenderer.materials = materialsCopy;
            }
            else
            {
                skinnedMeshRenderer.material = material;
            }
        }

        var meshRenderers = GetPrivateField<List<MeshRenderer>>(wearable, "MeshRenderers") ?? new List<MeshRenderer>();
        foreach (var meshRenderer in meshRenderers)
        {
            if (meshRenderer == null) continue;
            if (meshRenderer.materials.Length > 1)
            {
                var materialsCopy = meshRenderer.materials;
                for (var i = 0; i < materialsCopy.Length; ++i) materialsCopy[i] = material;
                meshRenderer.materials = materialsCopy;
            }
            else
            {
                meshRenderer.material = material;
            }
        }

        File.AppendAllText(tracePath, $"syncMaterialLoaded={materialName}\n");
    }

    private static void AttachWearableToSlot(Aavegotchi_WearableLoader loader, Aavegotchi_Wearable wearable, EWearableSlot slot)
    {
        if (slot == EWearableSlot.Hand_left && !wearable.IsSkinnedWeapon)
        {
            var target = wearable.WearableTypeHint switch
            {
                EWearableTypeHint.Hand_Shield => GetPrivateField<Transform>(loader, "LeftHand_Shield"),
                EWearableTypeHint.Hand_Grenade => GetPrivateField<Transform>(loader, "LeftHand_Grenade"),
                EWearableTypeHint.Hand_Ranged => GetPrivateField<Transform>(loader, "LeftHand_Ranged"),
                _ => GetPrivateField<Transform>(loader, "LeftHand_Melee"),
            };
            if (target != null) wearable.transform.SetParent(target, false);
            return;
        }

        if (slot == EWearableSlot.Hand_right && !wearable.IsSkinnedWeapon)
        {
            var target = wearable.WearableTypeHint switch
            {
                EWearableTypeHint.Hand_Shield => GetPrivateField<Transform>(loader, "RightHand_Shield"),
                EWearableTypeHint.Hand_Grenade => GetPrivateField<Transform>(loader, "RightHand_Grenade"),
                EWearableTypeHint.Hand_Ranged => GetPrivateField<Transform>(loader, "RightHand_Ranged"),
                _ => GetPrivateField<Transform>(loader, "RightHand_Melee"),
            };
            if (target != null) wearable.transform.SetParent(target, false);
            return;
        }

        if (slot == EWearableSlot.Pet)
        {
            var target = wearable.WearableTypeHint == EWearableTypeHint.Pet_Back ? loader.PetBackTransform : loader.PetTransform;
            if (target != null) wearable.transform.SetParent(target, false);
            return;
        }

        if (slot == EWearableSlot.Face && wearable.WearableTypeHint == EWearableTypeHint.Face_Mouth)
        {
            if (loader.MouthRoot != null) wearable.transform.SetParent(loader.MouthRoot, false);
            if (loader.DefaultSmile != null) loader.DefaultSmile.gameObject.SetActive(false);
            return;
        }

        if (slot == EWearableSlot.Body && wearable.WearableTypeHint == EWearableTypeHint.Body_Spine)
        {
            var target = GetPrivateField<Transform>(loader, "BodySpineRoot");
            if (target != null) wearable.transform.SetParent(target, false);
        }
    }

    private static void InvokeGotchiUpdateWearableLinks(string tracePath, Aavegotchi_Base gotchiBase)
    {
        var method = typeof(Aavegotchi_Base).GetMethod("UpdateWearableLinks", BindingFlags.Instance | BindingFlags.NonPublic);
        if (method == null)
        {
            File.AppendAllText(tracePath, "updateWearableLinksMissing=1\n");
            return;
        }

        method.Invoke(gotchiBase, null);
        File.AppendAllText(tracePath, "updateWearableLinksInvoked=1\n");
    }

    private static T GetPrivateField<T>(object instance, string fieldName) where T : class
    {
        var field = instance.GetType().GetField(fieldName, BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
        return field?.GetValue(instance) as T;
    }

    private static IEnumerable<(EWearableSlot slot, int wearableId)> RequestedWearableSlots(Aavegotchi_Data data)
    {
        yield return (EWearableSlot.Body, data.Body_WearableID);
        yield return (EWearableSlot.Face, data.Face_WearableID);
        yield return (EWearableSlot.Eyes, data.Eyes_WearableID);
        yield return (EWearableSlot.Head, data.Head_WearableID);
        yield return (EWearableSlot.Hand_left, data.HandLeft_WearableID);
        yield return (EWearableSlot.Hand_right, data.HandRight_WearableID);
        yield return (EWearableSlot.Pet, data.Pet_WearableID);
    }

    private static IEnumerable<int> RequestedWearableIds(Aavegotchi_Data data)
    {
        if (data.Body_WearableID > 0) yield return data.Body_WearableID;
        if (data.Face_WearableID > 0) yield return data.Face_WearableID;
        if (data.Eyes_WearableID > 0) yield return data.Eyes_WearableID;
        if (data.Head_WearableID > 0) yield return data.Head_WearableID;
        if (data.Pet_WearableID > 0) yield return data.Pet_WearableID;
        if (data.HandLeft_WearableID > 0) yield return data.HandLeft_WearableID;
        if (data.HandRight_WearableID > 0) yield return data.HandRight_WearableID;
    }

    private static void InitializeSdkComponents(string tracePath, Aavegotchi_Base gotchiBase)
    {
        InvokeAwakeIfPresent(tracePath, gotchiBase.Collaterals, nameof(Aavegotchi_Collaterals));

        var eyesField = typeof(Aavegotchi_Base).GetField("Eyes", BindingFlags.Instance | BindingFlags.NonPublic);
        var eyes = eyesField?.GetValue(gotchiBase) as MonoBehaviour;
        InvokeAwakeIfPresent(tracePath, eyes, "Aavegotchi_Eyes");
    }

    private static void InvokeAwakeIfPresent(string tracePath, MonoBehaviour behaviour, string label)
    {
        if (behaviour == null)
        {
            File.AppendAllText(tracePath, $"missing={label}\n");
            return;
        }

        var awake = behaviour.GetType().GetMethod("Awake", BindingFlags.Instance | BindingFlags.NonPublic | BindingFlags.Public);
        if (awake == null)
        {
            File.AppendAllText(tracePath, $"awakeMissing={label}\n");
            return;
        }

        awake.Invoke(behaviour, null);
        File.AppendAllText(tracePath, $"awakeInvoked={label}\n");
    }

    private static int RepairMissingShaders(string tracePath, GameObject root)
    {
        var repaired = 0;
        var hydratedFromAssets = 0;
        var unlitTexture = Shader.Find("Unlit/Texture");
        var unlitColor = Shader.Find("Unlit/Color");
        var legacyDiffuse = Shader.Find("Legacy Shaders/Diffuse");
        var standard = Shader.Find("Standard");
        var preferredLit = standard ?? legacyDiffuse;
        if (unlitTexture == null && unlitColor == null && legacyDiffuse == null && standard == null)
        {
            File.AppendAllText(tracePath, "repairShaderMissing=1\n");
            return repaired;
        }

        foreach (var renderer in root.GetComponentsInChildren<Renderer>(true))
        {
            var materials = renderer.sharedMaterials;
            var changed = false;

            for (var i = 0; i < materials.Length; i++)
            {
                var material = materials[i];
                if (material == null) continue;

                var shader = material.shader;
                var shaderName = shader != null ? shader.name : string.Empty;
                if (shader != null && shaderName != "Hidden/InternalErrorShader" && !shaderName.Contains("Error", StringComparison.OrdinalIgnoreCase))
                {
                    continue;
                }

                var baseMap = material.HasProperty("_BaseMap") ? material.GetTexture("_BaseMap") : null;
                var mainTex = material.HasProperty("_MainTex") ? material.GetTexture("_MainTex") : null;
                var resolvedTex = baseMap != null ? baseMap : mainTex;
                var replacementShader = resolvedTex != null
                    ? (preferredLit ?? unlitTexture ?? unlitColor)
                    : (preferredLit ?? unlitColor ?? unlitTexture);

                var replacement = new Material(replacementShader)
                {
                    name = $"{material.name}_Repaired"
                };

                if (resolvedTex != null && replacement.HasProperty("_MainTex"))
                {
                    replacement.SetTexture("_MainTex", resolvedTex);
                }

                if (resolvedTex != null && replacement.HasProperty("_BaseMap"))
                {
                    replacement.SetTexture("_BaseMap", resolvedTex);
                }

                if (material.HasProperty("_BaseColor") && replacement.HasProperty("_Color"))
                {
                    replacement.SetColor("_Color", material.GetColor("_BaseColor"));
                }
                else if (material.HasProperty("_Color") && replacement.HasProperty("_Color"))
                {
                    replacement.SetColor("_Color", material.GetColor("_Color"));
                }

                if (material.HasProperty("_EmissionColor") && replacement.HasProperty("_EmissionColor"))
                {
                    replacement.EnableKeyword("_EMISSION");
                    replacement.SetColor("_EmissionColor", material.GetColor("_EmissionColor"));
                }

                if (replacement.HasProperty("_Glossiness"))
                {
                    replacement.SetFloat("_Glossiness", 0.08f);
                }

                if (replacement.HasProperty("_Metallic"))
                {
                    replacement.SetFloat("_Metallic", 0f);
                }

                if (HydrateFallbackMaterialFromAsset(material, replacement))
                {
                    hydratedFromAssets++;
                }

                materials[i] = replacement;
                repaired++;
                changed = true;
            }

            if (changed)
            {
                renderer.sharedMaterials = materials;
            }
        }

        File.AppendAllText(tracePath, $"hydratedFallbackMaterials={hydratedFromAssets}\n");
        return repaired;
    }

    private static bool HydrateFallbackMaterialFromAsset(Material sourceMaterial, Material replacement)
    {
        var assetPath = AssetDatabase.GetAssetPath(sourceMaterial);
        if (string.IsNullOrWhiteSpace(assetPath))
        {
            var guids = AssetDatabase.FindAssets($"{sourceMaterial.name} t:Material");
            assetPath = guids.Select(AssetDatabase.GUIDToAssetPath).FirstOrDefault(path => path.EndsWith(".mat", StringComparison.OrdinalIgnoreCase));
        }

        if (string.IsNullOrWhiteSpace(assetPath) || !File.Exists(assetPath))
        {
            return false;
        }

        var yaml = File.ReadAllLines(assetPath);
        var hydrated = false;

        var baseTextureGuid = FindTextureGuid(yaml, "_BaseMap") ?? FindTextureGuid(yaml, "_MainTex");
        if (!string.IsNullOrWhiteSpace(baseTextureGuid) && replacement.HasProperty("_MainTex"))
        {
            var texPath = AssetDatabase.GUIDToAssetPath(baseTextureGuid);
            var texture = AssetDatabase.LoadAssetAtPath<Texture>(texPath);
            if (texture != null)
            {
                replacement.SetTexture("_MainTex", texture);
                hydrated = true;
            }
        }

        var baseColor = FindColor(yaml, "_BaseColor") ?? FindColor(yaml, "_Color");
        if (baseColor.HasValue && replacement.HasProperty("_Color"))
        {
            replacement.SetColor("_Color", baseColor.Value);
            hydrated = true;
        }

        var emissionColor = FindColor(yaml, "_EmissionColor");
        if (emissionColor.HasValue && replacement.HasProperty("_EmissionColor"))
        {
            replacement.EnableKeyword("_EMISSION");
            replacement.SetColor("_EmissionColor", emissionColor.Value);
            hydrated = true;
        }

        return hydrated;
    }

    private static string FindTextureGuid(string[] yaml, string propertyName)
    {
        for (var i = 0; i < yaml.Length; i++)
        {
            if (!yaml[i].Trim().StartsWith($"- {propertyName}:", StringComparison.Ordinal)) continue;

            for (var j = i + 1; j < yaml.Length; j++)
            {
                var trimmed = yaml[j].Trim();
                if (trimmed.StartsWith("- _", StringComparison.Ordinal)) break;

                if (!trimmed.StartsWith("m_Texture:", StringComparison.Ordinal)) continue;
                var match = Regex.Match(trimmed, @"guid:\s*([0-9a-fA-F]+)");
                if (match.Success)
                {
                    return match.Groups[1].Value;
                }
            }
        }

        return null;
    }

    private static Color? FindColor(string[] yaml, string propertyName)
    {
        for (var i = 0; i < yaml.Length; i++)
        {
            var trimmed = yaml[i].Trim();
            if (!trimmed.StartsWith($"- {propertyName}:", StringComparison.Ordinal)) continue;

            var match = Regex.Match(trimmed, @"r:\s*([-0-9.eE]+),\s*g:\s*([-0-9.eE]+),\s*b:\s*([-0-9.eE]+),\s*a:\s*([-0-9.eE]+)");
            if (!match.Success) return null;

            return new Color(
                float.Parse(match.Groups[1].Value, System.Globalization.CultureInfo.InvariantCulture),
                float.Parse(match.Groups[2].Value, System.Globalization.CultureInfo.InvariantCulture),
                float.Parse(match.Groups[3].Value, System.Globalization.CultureInfo.InvariantCulture),
                float.Parse(match.Groups[4].Value, System.Globalization.CultureInfo.InvariantCulture)
            );
        }

        return null;
    }

    private static string NormalizePose(string raw)
    {
        return NormalizeKey(string.IsNullOrWhiteSpace(raw) ? "idle" : raw) switch
        {
            "PORTRAIT" => "portrait",
            "HERO" => "hero",
            "LEFT" => "left",
            "RIGHT" => "right",
            _ => "idle",
        };
    }

    private static void ApplyPose(string tracePath, Aavegotchi_Base gotchiBase, string poseStyle)
    {
        var yaw = poseStyle switch
        {
            "hero" => -14f,
            "left" => 18f,
            "right" => -18f,
            _ => 0f,
        };

        gotchiBase.transform.localRotation = Quaternion.Euler(0f, yaw, 0f);
        File.AppendAllText(tracePath, $"poseStyle={poseStyle} yaw={yaw}\n");
    }

    private static void ConfigureStudioLighting(string tracePath, AavegotchiRenderTextureHolder holder, Color background)
    {
        var renderLayer = holder.gameObject.layer;
        RenderSettings.ambientMode = AmbientMode.Flat;
        RenderSettings.ambientLight = Color.Lerp(Color.white, background, 0.18f);

        ConfigureDirectionalLight(holder.transform, "KeyLight", renderLayer, new Color(1f, 0.96f, 0.92f), 1.15f, new Vector3(26f, -32f, 0f));
        ConfigureDirectionalLight(holder.transform, "FillLight", renderLayer, new Color(0.78f, 0.86f, 1f), 0.45f, new Vector3(20f, 38f, 0f));
        ConfigureDirectionalLight(holder.transform, "RimLight", renderLayer, new Color(1f, 1f, 1f), 0.65f, new Vector3(-18f, 155f, 0f));
        File.AppendAllText(tracePath, "studioLights=3\n");
    }

    private static void ConfigureDirectionalLight(Transform parent, string name, int renderLayer, Color color, float intensity, Vector3 eulerAngles)
    {
        var existing = parent.Find(name);
        var lightObject = existing != null ? existing.gameObject : new GameObject(name);
        if (existing == null)
        {
            lightObject.transform.SetParent(parent, false);
        }

        SetLayerRecursively(lightObject, renderLayer);
        lightObject.transform.localPosition = Vector3.zero;
        lightObject.transform.localRotation = Quaternion.Euler(eulerAngles);

        var light = lightObject.GetComponent<Light>();
        if (light == null)
        {
            light = lightObject.AddComponent<Light>();
        }

        light.type = LightType.Directional;
        light.color = color;
        light.intensity = intensity;
        light.shadows = LightShadows.None;
        light.cullingMask = 1 << renderLayer;
    }

    private static void CaptureFullAndHeadshot(string tracePath, AavegotchiRenderTextureHolder holder, Aavegotchi_Base gotchiBase, GotchiRenderRequest request, string poseStyle, Color background)
    {
        holder.gameObject.SetActive(true);
        holder.RenderCamera.gameObject.SetActive(true);
        holder.RenderCamera.enabled = true;
        holder.RenderCamera.clearFlags = CameraClearFlags.SolidColor;
        holder.RenderCamera.backgroundColor = background;
        holder.RenderCamera.nearClipPlane = 0.01f;
        holder.RenderCamera.farClipPlane = 100f;

        var bounds = CalculateBounds(gotchiBase.gameObject);
        File.AppendAllText(tracePath, $"bounds_center={bounds.center} bounds_size={bounds.size}\n");

        holder.Initialize(1600, 1600);
        PositionCameraForFull(holder.RenderCamera, bounds, poseStyle);
        SaveCurrentRender(holder, request.output.full_png);
        File.AppendAllText(tracePath, "saved full png\n");

        holder.Initialize(1024, 1024);
        PositionCameraForHeadshot(holder.RenderCamera, bounds, poseStyle);
        SaveCurrentRender(holder, request.output.headshot_png);
        File.AppendAllText(tracePath, "saved headshot png\n");
    }

    private static Bounds CalculateBounds(GameObject root)
    {
        var renderers = root.GetComponentsInChildren<Renderer>(true);
        var first = renderers.FirstOrDefault(r => r.enabled);
        if (first == null)
        {
            return new Bounds(root.transform.position + new Vector3(0f, 0.8f, 5f), new Vector3(2f, 2f, 2f));
        }

        var bounds = first.bounds;
        foreach (var renderer in renderers.Skip(1))
        {
            if (renderer.enabled)
            {
                bounds.Encapsulate(renderer.bounds);
            }
        }
        return bounds;
    }

    private static void PositionCameraForFull(Camera camera, Bounds bounds, string poseStyle)
    {
        camera.fieldOfView = 21f;
        var lateral = poseStyle == "hero" ? bounds.extents.x * 0.06f : 0f;
        var target = bounds.center + new Vector3(lateral, bounds.extents.y * 0.05f, 0f);
        var radius = Mathf.Max(bounds.extents.x * 1.12f, bounds.extents.y * 1.08f);
        PositionPerspectiveCamera(camera, target, radius, poseStyle == "hero" ? 1.08f : 1.16f);
    }

    private static void PositionCameraForHeadshot(Camera camera, Bounds bounds, string poseStyle)
    {
        camera.fieldOfView = 18f;
        var portraitLift = poseStyle == "portrait" ? 0.50f : 0.42f;
        var target = bounds.center + new Vector3(0f, bounds.extents.y * portraitLift, 0f);
        var radius = Mathf.Max(bounds.extents.x * 0.52f, bounds.extents.y * (poseStyle == "portrait" ? 0.36f : 0.42f));
        PositionPerspectiveCamera(camera, target, radius, poseStyle == "portrait" ? 0.92f : 1.05f);
    }

    private static void PositionPerspectiveCamera(Camera camera, Vector3 target, float radius, float distanceMultiplier)
    {
        var verticalFov = camera.fieldOfView * Mathf.Deg2Rad;
        var horizontalFov = 2f * Mathf.Atan(Mathf.Tan(verticalFov / 2f) * camera.aspect);
        var distanceV = radius / Mathf.Tan(verticalFov / 2f);
        var distanceH = radius / Mathf.Tan(horizontalFov / 2f);
        var distance = Mathf.Max(distanceV, distanceH) * distanceMultiplier;
        camera.transform.position = new Vector3(target.x, target.y, target.z - distance);
        camera.transform.rotation = Quaternion.LookRotation(target - camera.transform.position);
    }

    private static void SaveCurrentRender(AavegotchiRenderTextureHolder holder, string outputPath)
    {
        holder.RenderCamera.gameObject.SetActive(true);
        holder.RenderCamera.enabled = true;
        holder.PerformRender();

        var previous = RenderTexture.active;
        RenderTexture.active = holder.RenderTexture;
        var texture = new Texture2D(holder.RenderTexture.width, holder.RenderTexture.height, TextureFormat.RGBA32, false);
        texture.ReadPixels(new Rect(0, 0, holder.RenderTexture.width, holder.RenderTexture.height), 0, 0);
        texture.Apply();
        File.WriteAllBytes(outputPath, texture.EncodeToPNG());
        RenderTexture.active = previous;
        UnityEngine.Object.DestroyImmediate(texture);
    }

    private static Aavegotchi_Data BuildData(GotchiRenderRequest request)
    {
        var eyeShape = ParseEyeShape(request.eye_shape);
        var eyeColor = ParseEyeColor(request.eye_color, eyeShape);
        return new Aavegotchi_Data
        {
            HauntID = request.haunt_id,
            CollateralType = ParseCollateral(request.collateral),
            EyeShape = eyeShape,
            EyeColor = eyeColor,
            SkinID = request.skin_id,
            Body_WearableID = request.wearables.body,
            Face_WearableID = request.wearables.face,
            Eyes_WearableID = request.wearables.eyes,
            Head_WearableID = request.wearables.head,
            Pet_WearableID = request.wearables.pet,
            HandLeft_WearableID = request.wearables.hand_left,
            HandRight_WearableID = request.wearables.hand_right,
        };
    }

    private static ECollateral ParseCollateral(string raw)
    {
        if (string.IsNullOrWhiteSpace(raw)) return ECollateral.Eth;
        if (Enum.TryParse<ECollateral>(raw, true, out var parsed)) return parsed;
        switch (NormalizeKey(raw))
        {
            case "ETH": return ECollateral.Eth;
            case "AAVE": return ECollateral.Aave;
            case "DAI": return ECollateral.Dai;
            case "LINK": return ECollateral.Link;
            case "UNI": return ECollateral.Uni;
            case "YFI": return ECollateral.Yfi;
            case "POLYGON": return ECollateral.Polygon;
            case "WETH": return ECollateral.wEth;
            case "WBTC": return ECollateral.wBTC;
            default: return ECollateral.Eth;
        }
    }

    private static EEyeShape ParseEyeShape(string raw)
    {
        if (string.IsNullOrWhiteSpace(raw)) return EEyeShape.Common1;
        if (Enum.TryParse<EEyeShape>(raw, true, out var parsed)) return parsed;
        switch (NormalizeKey(raw))
        {
            case "ETH": return EEyeShape.ETH;
            case "AAVE": return EEyeShape.AAVE;
            case "DAI": return EEyeShape.DAI;
            case "LINK": return EEyeShape.LINK;
            case "USDT": return EEyeShape.USDT;
            case "USDC": return EEyeShape.USDC;
            case "TUSD": return EEyeShape.TUSD;
            case "UNI": return EEyeShape.UNI;
            case "YFI": return EEyeShape.YFI;
            case "POLYGON": return EEyeShape.POLYGON;
            case "WETH": return EEyeShape.wETH;
            case "WBTC": return EEyeShape.wBTC;
            case "COMMON": return EEyeShape.Common1;
            case "UNCOMMONLOW": return EEyeShape.UncommonLow1;
            case "UNCOMMONHIGH": return EEyeShape.UncommonHigh1;
            case "RARELOW": return EEyeShape.RareLow1;
            case "RAREHIGH": return EEyeShape.RareHigh1;
            case "MYTHICAL": return EEyeShape.MythicalLow1_H1;
            case "MYTHICALLOW": return EEyeShape.MythicalLow1_H1;
            case "MYTHICALHIGH": return EEyeShape.MythicalLow1_H1;
            default: return EEyeShape.Common1;
        }
    }

    private static EEyeColor ParseEyeColor(string raw, EEyeShape eyeShape)
    {
        if (string.IsNullOrWhiteSpace(raw)) return DefaultEyeColorForShape(eyeShape);
        if (Enum.TryParse<EEyeColor>(raw, true, out var parsed)) return parsed;
        switch (NormalizeKey(raw))
        {
            case "COMMON": return EEyeColor.Common;
            case "UNCOMMONLOW": return EEyeColor.Uncommon_Low;
            case "UNCOMMONHIGH": return EEyeColor.Uncommon_High;
            case "RARELOW": return EEyeColor.Rare_Low;
            case "RAREHIGH": return EEyeColor.Rare_High;
            case "MYTHICALLOW": return EEyeColor.Mythical_Low;
            case "MYTHICALHIGH": return EEyeColor.Mythical_High;
            case "LOW":
                return eyeShape.ToString().StartsWith("Mythical", StringComparison.OrdinalIgnoreCase)
                    ? EEyeColor.Mythical_Low
                    : eyeShape.ToString().StartsWith("Rare", StringComparison.OrdinalIgnoreCase)
                        ? EEyeColor.Rare_Low
                        : eyeShape.ToString().StartsWith("Uncommon", StringComparison.OrdinalIgnoreCase)
                            ? EEyeColor.Uncommon_Low
                            : EEyeColor.Common;
            case "HIGH":
                return eyeShape.ToString().StartsWith("Mythical", StringComparison.OrdinalIgnoreCase)
                    ? EEyeColor.Mythical_High
                    : eyeShape.ToString().StartsWith("Rare", StringComparison.OrdinalIgnoreCase)
                        ? EEyeColor.Rare_High
                        : eyeShape.ToString().StartsWith("Uncommon", StringComparison.OrdinalIgnoreCase)
                            ? EEyeColor.Uncommon_High
                            : EEyeColor.Common;
            default:
                return DefaultEyeColorForShape(eyeShape);
        }
    }

    private static EEyeColor DefaultEyeColorForShape(EEyeShape eyeShape)
    {
        var name = eyeShape.ToString();
        if (name.StartsWith("Mythical", StringComparison.OrdinalIgnoreCase)) return EEyeColor.Mythical_High;
        if (name.StartsWith("RareHigh", StringComparison.OrdinalIgnoreCase)) return EEyeColor.Rare_High;
        if (name.StartsWith("RareLow", StringComparison.OrdinalIgnoreCase)) return EEyeColor.Rare_Low;
        if (name.StartsWith("UncommonHigh", StringComparison.OrdinalIgnoreCase)) return EEyeColor.Uncommon_High;
        if (name.StartsWith("UncommonLow", StringComparison.OrdinalIgnoreCase)) return EEyeColor.Uncommon_Low;
        return EEyeColor.Common;
    }

    private static string NormalizeKey(string raw)
    {
        return (raw ?? string.Empty).Replace("_", string.Empty).Replace("-", string.Empty).Replace(" ", string.Empty).ToUpperInvariant();
    }

    private static string GetArgValue(string[] args, string key)
    {
        var idx = Array.IndexOf(args, key);
        return idx >= 0 && idx + 1 < args.Length ? args[idx + 1] : null;
    }

    private static void EnsureParent(string path)
    {
        var full = Path.GetFullPath(path);
        var dir = Path.GetDirectoryName(full);
        if (!string.IsNullOrEmpty(dir)) Directory.CreateDirectory(dir);
    }

    private static Color ParseBackground(string raw)
    {
        if (string.IsNullOrWhiteSpace(raw) || string.Equals(raw, "transparent", StringComparison.OrdinalIgnoreCase))
        {
            return new Color(0f, 0f, 0f, 0f);
        }
        return ColorUtility.TryParseHtmlString(raw, out var parsed) ? parsed : new Color(0f, 0f, 0f, 0f);
    }

    private static void Fail(string tracePath, string status, string message)
    {
        File.AppendAllText(tracePath, $"fail={status}:{message}\n");
        var result = new GotchiRenderResult
        {
            ok = false,
            status = status,
            message = message,
            unity_version = Application.unityVersion,
        };
        Console.WriteLine(JsonUtility.ToJson(result, true));
    }
}
