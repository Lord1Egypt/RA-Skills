#pragma once

#include "Modules/ModuleManager.h"

class FOpenClawUnrealEditorModule : public IModuleInterface
{
public:
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;

private:
    void RegisterMenus();
};
