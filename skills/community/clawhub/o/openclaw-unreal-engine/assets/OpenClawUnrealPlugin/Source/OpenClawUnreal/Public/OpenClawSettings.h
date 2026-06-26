#pragma once

#include "CoreMinimal.h"
#include "UObject/Object.h"
#include "OpenClawSettings.generated.h"

UCLASS(BlueprintType)
class OPENCLAWUNREAL_API UOpenClawSettings : public UObject
{
    GENERATED_BODY()

public:
    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString BaseUrl;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString ApiKey;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    bool bEnableWebSocket = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString WebSocketUrl;
};
