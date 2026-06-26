#include "OpenClawUnrealEditorModule.h"

#include "LevelEditor.h"
#include "ToolMenus.h"
#include "Modules/ModuleManager.h"

IMPLEMENT_MODULE(FOpenClawUnrealEditorModule, OpenClawUnrealEditor)

void FOpenClawUnrealEditorModule::StartupModule()
{
    if (UToolMenus::IsToolMenuUIEnabled())
    {
        RegisterMenus();
    }
}

void FOpenClawUnrealEditorModule::ShutdownModule()
{
}

void FOpenClawUnrealEditorModule::RegisterMenus()
{
    UToolMenu* Menu = UToolMenus::Get()->ExtendMenu("LevelEditor.MainMenu.Window");
    if (!Menu)
    {
        return;
    }

    FToolMenuSection& Section = Menu->FindOrAddSection("OpenClaw");
    Section.AddMenuEntry(
        "OpenClawPlaceholder",
        FText::FromString("OpenClaw"),
        FText::FromString("Placeholder entry for future OpenClaw editor tools."),
        FSlateIcon(),
        FUIAction());
}
