#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "OpenClawBlueprintLibrary.generated.h"

class UOpenClawSubsystem;

UCLASS()
class OPENCLAWUNREAL_API UOpenClawBlueprintLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "OpenClaw", meta = (WorldContext = "WorldContextObject"))
    static UOpenClawSubsystem* GetOpenClawSubsystem(UObject* WorldContextObject);
};
