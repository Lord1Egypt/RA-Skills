using UnrealBuildTool;

public class OpenClawUnrealEditor : ModuleRules
{
    public OpenClawUnrealEditor(ReadOnlyTargetRules Target) : base(Target)
    {
        PCHUsage = PCHUsageMode.UseExplicitOrSharedPCHs;

        PublicDependencyModuleNames.AddRange(new string[]
        {
            "Core"
        });

        PrivateDependencyModuleNames.AddRange(new string[]
        {
            "CoreUObject",
            "Engine",
            "UnrealEd",
            "LevelEditor",
            "ToolMenus",
            "Slate",
            "SlateCore",
            "OpenClawUnreal"
        });
    }
}
