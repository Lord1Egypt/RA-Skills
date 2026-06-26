#pragma once

#include "Modules/ModuleManager.h"

class FOpenClawUnrealModule : public IModuleInterface
{
public:
    virtual void StartupModule() override;
    virtual void ShutdownModule() override;
};
