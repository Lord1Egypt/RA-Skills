#include "OpenClawWebSocketClient.h"

#include "IWebSocket.h"
#include "WebSocketsModule.h"

FOpenClawWebSocketClient::FOpenClawWebSocketClient()
{
}

FOpenClawWebSocketClient::~FOpenClawWebSocketClient()
{
    Disconnect();
}

bool FOpenClawWebSocketClient::Connect(const FString& InUrl, const FString& InAuthToken)
{
    Url = InUrl;

    if (InUrl.IsEmpty())
    {
        return false;
    }

    if (!FModuleManager::Get().IsModuleLoaded(TEXT("WebSockets")))
    {
        FModuleManager::Get().LoadModule(TEXT("WebSockets"));
    }

    TArray<FString> Protocols;
    TMap<FString, FString> Headers;
    if (!InAuthToken.IsEmpty())
    {
        Headers.Add(TEXT("Authorization"), FString::Printf(TEXT("Bearer %s"), *InAuthToken));
    }

    Socket = FWebSocketsModule::Get().CreateWebSocket(InUrl, Protocols, Headers);
    Socket->OnConnected().AddLambda([this]()
    {
        if (OnConnected)
        {
            OnConnected();
        }
    });
    Socket->OnConnectionError().AddLambda([this](const FString& Error)
    {
        if (OnConnectionError)
        {
            OnConnectionError(Error);
        }
    });
    Socket->OnMessage().AddLambda([this](const FString& Message)
    {
        if (OnMessage)
        {
            OnMessage(Message);
        }
    });
    Socket->OnClosed().AddLambda([this](int32 StatusCode, const FString& Reason, bool bWasClean)
    {
        if (OnClosed)
        {
            OnClosed(Reason);
        }
    });

    Socket->Connect();
    return true;
}

void FOpenClawWebSocketClient::Disconnect()
{
    if (Socket.IsValid())
    {
        Socket->Close();
        Socket.Reset();
    }
}

bool FOpenClawWebSocketClient::Send(const FString& Message)
{
    if (!Socket.IsValid() || !Socket->IsConnected())
    {
        return false;
    }

    Socket->Send(Message);
    return true;
}

bool FOpenClawWebSocketClient::IsConnected() const
{
    return Socket.IsValid() && Socket->IsConnected();
}
