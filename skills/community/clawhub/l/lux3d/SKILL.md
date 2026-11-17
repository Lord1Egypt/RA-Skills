---
name: lux3d
description: "Use the Lux3D Global environment to generate 3D or a single image from image URLs or text, transfer materials onto an existing model, complete object viewpoints, split a GLB model into parts, retopologize static GLB meshes, rig GLB characters, retarget animations, export model formats, add joint motion to model parts, and query task status or generation history. Use for image-to-3D, text-to-3D, text plus reference image, single-image generation, material transfer, four-view completion, part splitting, mesh retopology/remesh, model articulation and joint motion, rigging, animation retargeting, USDZ/OBJ/FBX/STL/3MF export, task queries, or task lists."
---

# Lux3D Global

Use **lux3d_client.py** in this directory to call the public Lux3D API. Before running a command, change to this Skill directory or replace the script name in the examples with its absolute path. This package defaults to the Global environment:

~~~text
https://api.aholo.ai/global
~~~

Use only the public endpoints and fields listed here. Do not add business-type fields or internal versions.

## Before Calling

1. Apply for a key on the [Global API Key page](https://labs.aholo.ai/api-keys?from=lux3d).
2. Set the environment:

   ~~~bash
   export LUX3D_API_KEY="your_api_key"
   export LUX3D_REGION="international"
   ~~~

3. **img**, **imgs**, **meshUrl**, **glbUrl**, **modelUrl**, and **rigModelUrl** must be HTTP(S) URLs accessible to Lux3D. For a local file, upload it first with the [Asset upload APIs](https://labs.aholo.ai/api-docs/en/api-reference#tag/asset), then use the returned URL.
4. Global and China API Keys are not interchangeable. This Skill defaults to Global; do not mix it with the China endpoint.
5. Pass the API Key directly in the authentication header, without a Bearer prefix:

   ~~~text
   Authorization: <API Key>
   ~~~

Install the dependency:

~~~bash
pip install requests
~~~

## Choose a Capability

Select one creation endpoint for the request:

| Need | Capability |
| --- | --- |
| One or more object images and a 3D model | Image-to-3D |
| A text description, optionally with one reference image | Text-to-3D |
| An existing GLB that needs material transfer from an image | Material transfer |
| One new image from an image, text, or both | Multimodal single-image generation |
| Optional multi-view completion before a G1-Turbo generation request | Image-to-four-view -> G1-Turbo image-to-3D |
| Split one GLB model into separate parts | Part splitting |
| Rebuild a static GLB with a target topology and face budget | Mesh retopology |
| Additional formats from a Lux3D ZIP or GLB | Multi-format export |
| Add bones to a character GLB | Character model auto-rigging |
| Apply selected motions to a rigged GLB | Animation retargeting |
| Joint motion for GLB model parts based on a prompt | Model articulation |

For image-to-3D and text-to-3D, pass the input directly to **G1** without assembling other capabilities around it. **G1-Turbo** can run as a lightweight atomic capability on its own; when the user wants more control through multi-view input, they may optionally complete viewpoints first and pass the results as **imgs**. If the user did not specify a version and the request does not distinguish them, ask before creating the task.

A create endpoint returns a **taskid**. Query that task afterward; poll every 10-15 seconds.

**faceCount** is a target Mesh face count; the actual generated count may differ.

## 1. Image-to-3D

**version** is required. Pass **img** for a single image or **imgs** for multiple images, never both. **imgs** accepts 1-32 URLs of the same subject; put the clearest and most complete view first.

### G1

Pass only these fields:

| Field | Required | How to pass it |
| --- | :---: | --- |
| **img** | Conditional | One image URL; omit when using **imgs** |
| **imgs** | Conditional | 1-32 image URLs; omit when using **img** |
| **version** | Yes | Pass **G1** |
| **faceCount** | No | Target Mesh face count. Defaults to 300000 when omitted or null; explicit integers must be in [10000, 300000], otherwise the request is rejected. Does not affect PLY |
| **outputFormat** | No | A non-duplicated list of **zip**, **glb**, and **ply**. Omission, an empty list, or a list without **ply** returns ZIP + GLB; including **ply** returns ZIP + GLB + PLY |
| **aiPredictSize** | No | When **customSize** is omitted, omit or pass **true** to predict and scale size; pass **false** to disable |
| **customSize** | No | Model height in millimetres, greater than 0; when supplied, it takes priority over **aiPredictSize** |

Do not pass **enablePbr** for G1. Output order is always ZIP, GLB, optional PLY. Even ["ply"] returns all three outputs.

~~~bash
python lux3d_client.py image \
  "https://example.com/object.jpg" \
  --version G1
~~~

Multiple images:

~~~bash
python lux3d_client.py image \
  "https://example.com/front.jpg" \
  --image-view "https://example.com/side.jpg" \
  --version G1 --format ply
~~~

### G1-Turbo

Pass only these fields:

| Field | Required | How to pass it |
| --- | :---: | --- |
| **img** | Conditional | One image URL; omit when using **imgs** |
| **imgs** | Conditional | 1-32 image URLs; omit when using **img** |
| **version** | Yes | Pass **G1-Turbo** |
| **faceCount** | No | Target Mesh face count. Defaults to 300000 when omitted or null; explicit integers must be in [10000, 300000], otherwise the request is rejected. Does not affect PLY |
| **outputFormat** | No | Any non-duplicated individual or combined **zip**, **glb**, and **ply** values; omission or an empty list is treated as ["zip"] |
| **enablePbr** | No | For ZIP/GLB, omit or pass **true** for a textured Mesh and **false** for a white Mesh; omit for PLY-only |
| **aiPredictSize** | No | Omit or pass **true** to predict and scale size; pass **false** to disable |

~~~bash
python lux3d_client.py image \
  "https://example.com/object.jpg" \
  --version G1-Turbo --format glb --no-pbr
~~~

PLY-only:

~~~bash
python lux3d_client.py image \
  "https://example.com/object.jpg" \
  --version G1-Turbo --format ply
~~~

## 2. Text-to-3D

**prompt** and **version** are required. **style** is optional. For visual guidance, pass one **img** URL; do not pass **imgs**.

Supported **style** values:

~~~text
photorealistic, cartoon, anime, hand_painted, cyberpunk, fantasy, glass
~~~

The default style is **photorealistic**.

### G1

| Field | Required | How to pass it |
| --- | :---: | --- |
| **prompt** | Yes | Non-empty text describing the subject, material, style, and key details |
| **style** | No | Use one value from the list above |
| **img** | No | One accessible reference-image URL |
| **version** | Yes | Pass **G1** |
| **faceCount** | No | Target Mesh face count. Defaults to 300000 when omitted or null; explicit integers must be in [10000, 300000], otherwise the request is rejected. Does not affect PLY |
| **outputFormat** | No | A non-duplicated list of **zip**, **glb**, and **ply**. A list without **ply** returns ZIP + GLB; including **ply** appends PLY |
| **aiPredictSize** | No | When **customSize** is omitted, omit or pass **true** to predict and scale size; pass **false** to disable |
| **customSize** | No | Model height in millimetres, greater than 0; when supplied, it takes priority over **aiPredictSize** |

Do not pass **enablePbr**.

~~~bash
python lux3d_client.py text \
  "A modern dining chair with visible wood grain" \
  --style photorealistic --version G1
~~~

### G1-Turbo

| Field | Required | How to pass it |
| --- | :---: | --- |
| **prompt** | Yes | Non-empty text describing the subject, material, style, and key details |
| **style** | No | Use one value from the list above |
| **img** | No | One accessible reference-image URL |
| **version** | Yes | Pass **G1-Turbo** |
| **faceCount** | No | Target Mesh face count. Defaults to 300000 when omitted or null; explicit integers must be in [10000, 300000], otherwise the request is rejected. Does not affect PLY |
| **outputFormat** | No | Any non-duplicated individual or combined **zip**, **glb**, and **ply** values; omission or an empty list is treated as ["zip"] |
| **enablePbr** | No | For ZIP/GLB, omit or pass **true** for a textured Mesh and **false** for a white Mesh; omit for PLY-only |
| **aiPredictSize** | No | Omit or pass **true** to predict and scale size; pass **false** to disable |

~~~bash
python lux3d_client.py text \
  "A futuristic desk lamp" \
  --image "https://example.com/reference.png" \
  --version G1-Turbo --format glb
~~~

## 3. Material Transfer

This endpoint uses only **v3.0-standard**:

| Field | Required | How to pass it |
| --- | :---: | --- |
| **img** | Yes | Material reference-image URL |
| **meshUrl** | Yes | URL of the GLB to retexture |
| **version** | Yes | Pass **v3.0-standard** |
| **outputFormat** | No | A non-duplicated list of **zip**, **glb**, **usdz**, **obj_zip**, and **fbx_zip**. Omission or an empty list returns ZIP + GLB; include other values when needed |
| **aiPredictSize** | No | Pass **true** for automatic size prediction and omit **customSize**; pass **false** or omit to preserve size or set a height |
| **customSize** | No | Model height in millimetres, greater than 0; set **aiPredictSize** to **false** or omit it |

~~~bash
python lux3d_client.py material \
  "https://example.com/material.png" \
  --mesh-url "https://example.com/model.glb" \
  --version v3.0-standard --format usdz
~~~

## 4. Multimodal Single-Image Generation

Generate one new image from an image, text, or both. Pass at least one of **img** and **prompt**:

| Field | Required | How to pass it |
| --- | :---: | --- |
| **img** | Conditional | One accessible reference-image URL; omit for text-only generation |
| **prompt** | Conditional | A non-empty generation request; omit for image-only generation |

With image-only input, the endpoint generates a new image from the reference instead of returning the original image. A successful task returns one image URL.

~~~bash
python lux3d_client.py multimodal-image \
  --image "https://example.com/reference.jpg" \
  --prompt "Preserve the shape and change the material to light natural wood"
~~~

Text-only generation:

~~~bash
python lux3d_client.py multimodal-image \
  --prompt "A light natural-wood dining chair on a pure white background"
~~~

~~~python
from lux3d_client import generate_multimodal_image

image_url = generate_multimodal_image(
    prompt="A light natural-wood dining chair on a pure white background"
)
print(image_url)
~~~

## 5. Image-to-Four-View

Complete object viewpoints from an image, text, or both. This endpoint does not generate a 3D model. Pass at least one of **img** and **prompt**:

| Field | Required | How to pass it |
| --- | :---: | --- |
| **img** | Conditional | One accessible object-image URL; omit for text-only generation |
| **prompt** | Conditional | A non-empty subject description or generation request; omit for image-only generation |

~~~bash
python lux3d_client.py four-view "https://example.com/object.jpg"
~~~

Text-only generation:

~~~bash
python lux3d_client.py four-view --prompt "A light natural-wood dining chair"
~~~

On success, it returns four image URLs in this fixed order: front three-quarter, opposite three-quarter, side, and back. The API stores them as a JSON-array string in one output item; the client parses that value into a list.

G1-Turbo accepts either one image or multiple images directly. Check the input first: when it has a plain background, or its background has been removed and it contains only the target object to generate, pass the single image directly as **img**. Viewpoints and structural details that are not visible in the image are inferred from the available information. Offer the following composition when the user wants to reduce that inference, gain more control over unseen viewpoints, or provide missing viewpoint information:

~~~text
Image or text -> Image-to-four-view -> Review and approve -> imgs -> G1-Turbo image-to-3D
~~~

~~~python
from lux3d_client import generate_four_views

four_view_urls = generate_four_views("https://example.com/object.jpg")
print(four_view_urls)
~~~

Show the four images or their URLs to the user and confirm that the subject structure, orientation, and viewpoints match expectations. Do not create the G1-Turbo task until the user explicitly approves the results. After approval, continue with:

~~~python
from lux3d_client import create_image_to_3d_task

task_id = create_image_to_3d_task(
    imgs=four_view_urls,
    version="G1-Turbo",
)
~~~

If the order needs adjustment, put the clearest and most complete view first in **imgs**.

This is only a recommended optional enhancement, not a prerequisite for G1-Turbo. If the user asks to call G1-Turbo directly, pass the single image as **img**; do not force multi-view completion or block the call because four-view results are absent. For G1, pass the original input directly and do not add a four-view task to the workflow.

## 6. Part Splitting

Pass one GLB model URL accessible to Lux3D and receive one reconstructed GLB containing the part-splitting result. The request contains only **glbUrl**; intermediate processing artifacts are not exposed.

| Field | Required | How to pass it |
| --- | :---: | --- |
| **glbUrl** | Yes | URL of the GLB model to split. Upload a local model with the Asset upload APIs first |

Without an output path, the command returns the final reconstructed GLB URL:

~~~bash
python lux3d_client.py part-split "https://example.com/model.glb"
~~~

With an output path, the command downloads one final GLB. If the path has no extension, **.glb** is appended:

~~~bash
python lux3d_client.py part-split \
  "https://example.com/model.glb" \
  "reconstructed-parts.glb"
~~~

~~~python
from lux3d_client import generate_part_split

glb_url = generate_part_split("https://example.com/model.glb")
download = generate_part_split(
    "https://example.com/model.glb",
    output_path="reconstructed-parts.glb",
)
~~~

If the authenticated account already has a part-splitting task in progress, no task is created. Wait for it to finish and retry.

## 7. Multi-Format Export

**modelUrl** must be an accessible .zip or .glb URL. A ZIP input must come from a Lux3D generation task.

| Input | **outputFormat** rule |
| --- | --- |
| GLB | Pass at least one of **usdz**, **obj_zip**, **fbx_zip**, **stl**, or **3mf** |
| ZIP | Omit or pass an empty list to return GLB, or request one or more export formats above |

~~~bash
python lux3d_client.py export \
  "https://example.com/model.glb" \
  --format usdz --format stl --format 3mf
~~~

The response contains fixed ZIP, GLB, USDZ, OBJ ZIP, FBX ZIP, STL, and 3MF output slots. The client ignores empty values, the string **null**, and **NOT_REQUESTED** for formats that were not requested, returning only usable URLs.

## Character Model Auto-Rigging and Animation Retargeting

### Auto-rigging

Provide a publicly downloadable HTTPS GLB. Creation returns `taskId` immediately:

~~~bash
python lux3d_client.py auto-rig "https://example.com/character.glb"
python lux3d_client.py rig-result <taskId>
python lux3d_client.py rig-result <taskId> "rigged.glb"
~~~

Without an output path, the result command returns the rigged GLB URL; with a path,
it downloads the original file. Python callers can use
`create_auto_rig_task(modelUrl, content_id=None)` followed by
`complete_task(task_id, expected_formats=["glb"], output_path="rigged.glb")`.

### Animation retargeting

Provide an already rigged HTTPS GLB. Select 1–10 distinct, case-sensitive IDs from
[the 85 public animation IDs](animation_ids.json) bundled beside the client.
Repeat `--animation-id`; the requested order is retained.

| Field | Required | How to pass it |
| --- | :---: | --- |
| **rigModelUrl** | Yes | Publicly downloadable, rigged HTTPS GLB URL |
| **animationIds** | Yes | 1–10 distinct public animation IDs |
| **animationOutputMode** | No | **separate** (default): one file per action; **combined**: independent clips in one file |
| **outFormat** | No | **glb** (default) or bare **fbx** |
| **animateInPlace** | No | In-place animation; defaults to **false** |
| **contentId** | No | Current quote correlation identifier, such as quoteId; not an idempotency key |

~~~bash
python lux3d_client.py retarget "https://example.com/rigged.glb" \
  --animation-id Dance_Loop --animation-id Idle_Loop

python lux3d_client.py retarget-result <taskId> "animated" \
  --animation-id Dance_Loop --animation-id Idle_Loop
~~~

For combined FBX, add `--output-mode combined --format fbx` to both creation and
result recovery. Add `--animate-in-place` to creation for in-place animation.
An existing quote can be correlated with `--content-id <quoteId>` on either
creation command. Python equivalents are
`create_animation_retarget_task(rigModelUrl, animationIds, ...)` and
`resume_animation_retarget(task_id, animationIds, output_path=None, ...)`.

Creation only returns the task ID. Save it before running a result command.
For a complete character flow, rig first, wait for success, then pass the actual
rigged GLB URL to retargeting. Do not retarget after rigging fails. Resume the
original task after query or download failures; do not automatically create again.
Reconcile task history when creation acceptance is unknown. Use the original
account and region. Character model statuses 0/1/2 are waiting, 3 is provider
completion, 4/5 are failure, and 6 is cancellation. Result commands accept
`--max-attempts` and `--interval` for polling.

Retargeting `outputs[0].content` is a JSON string containing `actions`. Preserve
each `animation_id` and `status`; success uses `animationGlbUrl` or `fbxUrl`, and
failure retains the real `error.code/message`. The result's `completion` is
`complete`, `partial`, or `failed`; provider status 3 does not imply every action
succeeded. Missing, duplicate, unknown actions or mismatched formats are rejected,
never filled with invented successes. Separate files retain action labels;
combined duplicate URLs are downloaded once with every associated action ID.
Bare **fbx** is an original file, not **fbx_zip**; do not unzip it or substitute
an intermediate GLB. Downloading a file does not verify its skeleton or animation.
When validation is required, open it in the target DCC or Blender and inspect
skinning, bones and independent clips. This Skill does not bundle an animation viewer.

Keep `SKILL.md`, `lux3d_client.py` and `animation_ids.json` in the same installation
directory. The catalog is synchronized with the plugin's public OpenAPI contract;
the client reads it directly instead of maintaining another animation enum.

## 8. Model Articulation

Add joints and motion to parts of a GLB model. Call **POST /global/lux3d/v1/articulation-animation/task/create**. The request body contains only these fields:

| Field | Required | How to pass it |
| --- | :---: | --- |
| **glbUrl** | Yes | Accessible HTTP(S) URL of the input GLB; upload local files first and preserve the camelCase field name |
| **prompt** | Yes | Non-empty motion instructions identifying moving parts, fixed parts, and the intended joint motion |

Use only the request fields listed above. Model articulation is distinct from character rigging and animation retargeting.

~~~bash
python lux3d_client.py articulation \
  "https://example.com/box.glb" \
  --prompt "Keep the base fixed, add a hinge to the lid, and slowly open and close it."
~~~

By default, creation is followed by polling every 15 seconds for up to 60 attempts. The task ID is printed to standard error after creation. A polling timeout does not mean the task failed: retain that ID and query it instead of creating another task. Use **--max-attempts 240 --interval 15** for a longer wait. To submit without waiting, add **--submit-only**; the command returns the task ID, which can be queried with **query <taskid>**.

On success, **d.outputs[0].content** contains one final file URL. The artifact may be ZIP, GLB, or another format; do not always unzip it. On failure or cancellation, report the task status and error rather than downloading intermediate outputs.

Optionally supply a download filename base:

~~~bash
python lux3d_client.py articulation \
  "https://example.com/box.glb" "joint-motion" \
  --prompt "Keep the base fixed and open the lid around its hinge."
~~~

Downloads use the existing download helper. The filename suffix comes from the actual result URL, excluding query parameters; unknown suffixes use **.bin**. No format conversion is performed. Without a download path, the command returns the original result URL. Result URLs expire after 2 hours, so save them promptly.

~~~python
from lux3d_client import create_articulation_animation_task, query_task_status, parse_articulation_animation_output

task_id = create_articulation_animation_task(
    glbUrl="https://example.com/box.glb",
    prompt="Keep the base fixed and open the lid around its hinge.",
)
result_url = query_task_status(
    task_id, max_attempts=240, interval=15,
    output_parser=parse_articulation_animation_output,
)
~~~

## 9. Query One Task

Query once:

~~~bash
python lux3d_client.py query 1256173
~~~

Poll from Python:

~~~python
from lux3d_client import query_task_status

outputs = query_task_status("1256173")
~~~

Public statuses:

| Status | Meaning |
| --- | --- |
| 0 | Initialized |
| 1 | Running |
| 3 | Succeeded |
| 4 | Failed |
| 6 | Cancelled |

After success, read results from **d.outputs[].content**. Result URLs expire after 2 hours, so save them promptly.

## 10. List Generation Tasks

~~~bash
python lux3d_client.py list \
  --page 1 --pagesize 20 --status 3 \
  --starttime 1786590000000 --endtime 1786600000000
~~~

- **page** is one-based and defaults to 1
- **pagesize** is 1-100 and defaults to 20
- **status** may be 0, 1, 3, 4, or 6
- Times are Unix milliseconds and use the interval [starttime, endtime)
- Omit unused filters

## Python Functions

Use the functions in endpoint order:

~~~python
from lux3d_client import (
    create_image_to_3d_task,
    create_text_to_3d_task,
    create_material_transfer_task,
    create_multimodal_to_image_task,
    create_image_to_four_view_task,
    create_part_split_task,
    create_mesh_retopology_task,
    create_multi_format_export_task,
    create_auto_rig_task,
    create_animation_retarget_task,
    resume_animation_retarget,
    complete_task,
    create_articulation_animation_task,
    generate_3d_model,
    generate_text_to_3d,
    generate_material_transfer,
    generate_multimodal_image,
    generate_four_views,
    generate_part_split,
    generate_multi_format_export,
    generate_articulation_animation,
    get_task,
    list_tasks,
)
~~~

Pass only the fields listed for the selected version. For example:

~~~python
task_id = create_image_to_3d_task(
    img="https://example.com/object.jpg",
    version="G1",
    outputFormat=["ply"],
    customSize=850,
)
~~~

## Tasks and Credits

The following creation endpoints share the account concurrency limit: image-to-3D, text-to-3D, material transfer, multimodal single-image generation, image-to-four-view, mesh retopology, model articulation, character model auto-rigging, and animation retargeting. Part splitting has a separate per-account in-progress task limit; if the authenticated account already has a part-splitting task in progress, wait for it to finish and retry. Multi-format export, task queries, and task-list requests do not use the shared generation concurrency allowance.

| Account | Concurrent in-progress tasks |
| --- | :---: |
| Free | 2 |
| Pro | 10 |

If the API returns **GENERATION_CONCURRENCY_LIMIT_EXCEEDED**, wait for an existing task to finish before retrying. The rejected request does not create a task or consume credits. See [Lux3D Pricing](https://lux3d.aholo.ai/lux3d/home?view=pricing&lang=en_US) for plans and credits.

## References

- [API Key](https://labs.aholo.ai/api-keys?from=lux3d)
- [Asset upload APIs](https://labs.aholo.ai/api-docs/en/api-reference#tag/asset)
- [Lux3D Pricing](https://lux3d.aholo.ai/lux3d/home?view=pricing&lang=en_US)
- Contact: lux3d@qunhemail.com


## Static GLB mesh retopology

Use retopology to rebuild an existing model's mesh, not material transfer, part splitting,
or format conversion. Input must be static, non-Draco GLB; bones, skinning, animation and
morph targets are unsupported. Original part boundaries need not be preserved.
Ask for or confirm the face budget before creating a paid task: quad 1000–500000;
triangle 2000–1000000. There is no default budget. Do not invent user approval for 5000.
The budget is not an exact face-count or all-quad guarantee.

- API helper: `create_mesh_retopology_task(modelUrl, faceLimit, quad=True, bakeTextures=False, textureSize=2048)`.
- CLI: `python lux3d_client.py retopology <GLB_URL> <output-basename> --face-limit 5000`.
  Add `--triangle` for triangles, or `--bake-textures --texture-size 2048` for baking.
  Only 512/1024/2048/4096 are valid sizes, including when baking is disabled.
- Upload local inputs using the existing regional upload path. Preserve existing regional
  credentials and paid-action confirmation. Do not send version or algorithm options.
  Optional `--content-id` is correlation metadata, not an idempotency key.
- Record taskId immediately after creation. The convenience CLI prints it to stderr before
  polling. If POST outcome is unknown, reconcile task history; never blindly submit again.
- Resume with `python lux3d_client.py retopology-result <taskId> <output-basename>`.
  Add `--bake-textures` if the original request asked for baking. Query/download failures
  resume the original task, preserving downloaded files; they never justify another paid create.

Outputs are exactly three fixed slots: GLB, untextured OBJ, optional OBJ ZIP. Only the third
slot may be an empty string. Helpers return named `artifacts` and `warnings`, and download
both mandatory artifacts plus the ZIP when present. Do not filter/reorder slots or download
an empty URL. OBJ is the formal topology geometry; GLB is always triangulated.
`TEXTURE_PACKAGE_NOT_GENERATED` means baking was requested but no texture package was
returned: deliver the geometry and disclose the missing package without claiming completed
baking or resubmitting. Report public task failure honestly; do not infer private scores or refunds.
