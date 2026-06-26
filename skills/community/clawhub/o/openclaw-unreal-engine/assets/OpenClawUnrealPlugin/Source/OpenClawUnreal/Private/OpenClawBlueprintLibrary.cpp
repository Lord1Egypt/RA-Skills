#include "OpenClawBlueprintLibrary.h"

#include "Engine/Engine.h"
#include "Engine/GameInstance.h"
#include "Kismet/GameplayStatics.h"
#include "OpenClawSubsystem.h"

UOpenClawSubsystem* UOpenClawBlueprintLibrary::GetOpenClawSubsystem(UObject* WorldContextObject)
{
    if (!WorldContextObject)
    {
        return nullptr;
    }

    UGameInstance* GameInstance = UGameplayStatics::GetGameInstance(WorldContextObject);
    if (!GameInstance)
    {
        return nullptr;
    }

    return GameInstance->GetSubsystem<UOpenClawSubsystem>();
}
