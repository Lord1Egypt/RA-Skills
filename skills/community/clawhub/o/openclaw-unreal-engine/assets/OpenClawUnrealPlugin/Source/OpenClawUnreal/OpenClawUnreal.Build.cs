using UnrealBuildTool;

public class OpenClawUnreal : ModuleRules
{
    public OpenClawUnreal(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core",
            "CoreUObject",
            "Engine"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "HTTP",
            "Json",
            "JsonUtilities",
            "WebSockets",
            "RemoteControl",
            "HttpBlueprint",
            "JsonBlueprintUtilities"
        });
    }
}
