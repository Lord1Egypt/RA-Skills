#pragma once

#include "CoreMinimal.h"
#include "Kismet/BlueprintFunctionLibrary.h"
#include "OpenClawEditorTaskLibrary.generated.h"

UCLASS()
class OPENCLAWUNREAL_API UOpenClawEditorTaskLibrary : public UBlueprintFunctionLibrary
{
    GENERATED_BODY()

public:
    UFUNCTION(BlueprintCallable, Category = "OpenClaw|Editor")
    static FString BuildRemoteControlCallEnvelope(const FString& RequestId, const FString& ObjectPath, const FString& FunctionName, const FString& ParametersJson);

    UFUNCTION(BlueprintCallable, Category = "OpenClaw|Editor")
    static FString BuildRemoteControlSetPropertyEnvelope(const FString& RequestId, const FString& ObjectPath, const FString& PropertyName, const FString& PropertyValueJson);
};
