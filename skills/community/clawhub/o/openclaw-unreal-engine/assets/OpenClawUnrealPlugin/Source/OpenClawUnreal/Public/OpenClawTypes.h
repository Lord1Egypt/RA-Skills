#pragma once

#include "CoreMinimal.h"
#include "OpenClawTypes.generated.h"

UENUM(BlueprintType)
enum class EOpenClawConnectionStatus : uint8
{
    Disconnected,
    Configured,
    Connected,
    Error
};

USTRUCT(BlueprintType)
struct FOpenClawTaskRequest
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString RequestId;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString Type;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString Task;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString PayloadJson;
};

USTRUCT(BlueprintType)
struct FOpenClawTaskResponse
{
    GENERATED_BODY()

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    bool bOk = false;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString RequestId;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString ResultJson;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "OpenClaw")
    FString ErrorMessage;
};
