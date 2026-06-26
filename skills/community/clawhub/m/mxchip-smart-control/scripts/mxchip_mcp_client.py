#!/usr/bin/env python3
"""
Mxchip Smart Control MCP Client SDK
Official MCP client for controlling smart home devices via MXCHIP MCP service.

Developer: Shanghai MXCHIP Information Technology Co., Ltd. (上海庆科信息技术有限公司)
Website: https://www.mxchip.com/
GitHub: https://github.com/mxchip

This SDK implements MCP (Model Context Protocol) with JSON-RPC 2.0 over HTTP
for controlling devices configured in Smart Plus APP (智家精灵).
"""

import os
import json
import uuid
import requests
from typing import Dict, List, Optional, Any, Generator


class MxchipMCPError(Exception):
    """Base exception for Mxchip MCP errors"""
    pass


class AuthenticationError(MxchipMCPError):
    """Authentication failed"""
    pass


class DeviceNotFoundError(MxchipMCPError):
    """Device not found"""
    pass


class InvalidParameterError(MxchipMCPError):
    """Invalid parameter"""
    pass


class MxchipMCPClient:
    """
    MCP client for Mxchip smart home control.
    
    Implements MCP protocol with JSON-RPC 2.0 over Streamable HTTP.
    
    Usage:
        client = MxchipMCPClient()
        
        # List devices and scenes
        result = client.list_home_devices_and_scenes()
        
        # Control device
        client.control_device("device_id", "TurnOnRequest")
        
        # Control air conditioner
        client.control_air_conditioner(
            "ac_id",
            "SetTemperatureRequest",
            temperature=26
        )
        
        # Trigger scene
        client.trigger_scene("sceneid_xxx")
    """

    def __init__(
        self,
        oauth_token: Optional[str] = None,
        base_url: str = "https://app.api.cloud.mxchip.com:2443/mcp"
    ):
        """
        Initialize MCP client.
        
        Args:
            oauth_token: OAuth2 token (reads from MXCHIP_OAUTH_TOKEN env var)
            base_url: MCP server URL
        
        Raises:
            AuthenticationError: If OAuth token is not provided
        """
        self.oauth_token = oauth_token or os.getenv("MXCHIP_OAUTH_TOKEN")
        if not self.oauth_token:
            raise AuthenticationError(
                "OAuth token required. Set MXCHIP_OAUTH_TOKEN environment variable "
                "or pass oauth_token parameter. Get token at: "
                "https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth"
            )

        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {self.oauth_token}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream"
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def _make_jsonrpc_request(
        self,
        method: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make JSON-RPC 2.0 request to MCP server.
        
        Args:
            method: MCP method name
            params: Method parameters
        
        Returns:
            JSON-RPC response result
        
        Raises:
            AuthenticationError: If authentication fails
            MxchipMCPError: For other errors
        """
        request_id = str(uuid.uuid4())
        
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "id": request_id
        }
        
        if params:
            payload["params"] = params

        try:
            response = self.session.post(
                self.base_url,
                json=payload,
                timeout=30
            )

            if response.status_code == 401:
                raise AuthenticationError(
                    "Authentication failed. Check your OAuth token or regenerate at: "
                    "https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth"
                )

            response.raise_for_status()
            
            # Parse response
            data = response.json()
            
            # Check for JSON-RPC error
            if "error" in data:
                error = data["error"]
                raise MxchipMCPError(
                    f"MCP Error {error.get('code')}: {error.get('message')}"
                )
            
            result = data.get("result", {})
            
            # Parse nested JSON in content if present
            # Response format: {"result": {"content": [{"type": "text", "text": "{...}"}]}}
            if "content" in result and len(result["content"]) > 0:
                content_item = result["content"][0]
                if content_item.get("type") == "text":
                    text_data = content_item.get("text", "{}")
                    try:
                        parsed_data = json.loads(text_data)
                        return parsed_data
                    except json.JSONDecodeError:
                        # If parsing fails, return as is
                        return result
            
            return result

        except requests.exceptions.RequestException as e:
            raise MxchipMCPError(f"Request failed: {str(e)}")
        except json.JSONDecodeError as e:
            raise MxchipMCPError(f"Invalid JSON response: {str(e)}")

    def list_home_devices_and_scenes(self) -> Dict[str, Any]:
        """
        List all home devices and scenes.
        
        Returns:
            Dictionary containing:
            - devices: List of device objects with device_id, name, category, status
            - scenes: List of scene objects with scene_id, name
        
        Example:
            >>> result = client.list_home_devices_and_scenes()
            >>> for device in result.get('devices', []):
            ...     print(f"{device['name']}: {device['category']}")
            >>> for scene in result.get('scenes', []):
            ...     print(f"{scene['name']}: {scene['scene_id']}")
        """
        response = self._make_jsonrpc_request("tools/call", {
            "name": "list_home_devices_and_scenes",
            "arguments": {}
        })
        
        # Parse the nested JSON structure
        # Response format: {"content": [{"type": "text", "text": "{\"devices\":[...], \"scenes\":[...]}"}]}
        if "content" in response and len(response["content"]) > 0:
            content = response["content"][0]
            if content.get("type") == "text" and "text" in content:
                # Parse the JSON string in the text field
                return json.loads(content["text"])
        
        return response

    def control_device(
        self,
        device_id: str,
        action: str
    ) -> Dict[str, Any]:
        """
        Control device power state (on/off).
        
        Args:
            device_id: Device unique identifier (from list_home_devices_and_scenes)
            action: "TurnOnRequest" (turn on) or "TurnOffRequest" (turn off)
        
        Returns:
            Control result
        
        Raises:
            InvalidParameterError: If action is invalid
        
        Examples:
            # Turn on device
            >>> client.control_device("device_001", "TurnOnRequest")
            
            # Turn off device
            >>> client.control_device("device_001", "TurnOffRequest")
        """
        if action not in ["TurnOnRequest", "TurnOffRequest"]:
            raise InvalidParameterError(
                f"Invalid action '{action}'. Must be 'TurnOnRequest' or 'TurnOffRequest'"
            )
        
        return self._make_jsonrpc_request("tools/call", {
            "name": "control_device",
            "arguments": {
                "device_id": device_id,
                "action": action
            }
        })

    def control_air_conditioner(
        self,
        device_id: str,
        action: str,
        temperature: Optional[int] = None,
        delta: Optional[str] = None,
        mode: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Control air conditioner temperature and mode.
        
        Args:
            device_id: Air conditioner device ID (AIR_CONDITION category)
            action: Control action type
                - "IncrementTemperatureRequest": Increase temperature
                - "DecrementTemperatureRequest": Decrease temperature
                - "SetTemperatureRequest": Set target temperature
                - "SetModeRequest": Set working mode
            temperature: Target temperature (16-32°C), for SetTemperatureRequest
            delta: Temperature change amount (default 1°C), for Increment/Decrement
            mode: Working mode, for SetModeRequest
                - "COOL": Cooling
                - "HEAT": Heating
                - "AUTO": Auto
                - "FAN": Fan only
                - "DEHUMIDIFICATION": Dehumidify
                - "SLEEP": Sleep mode
        
        Returns:
            Control result
        
        Raises:
            InvalidParameterError: If parameters are invalid
        
        Examples:
            # Set temperature to 26°C
            >>> client.control_air_conditioner("ac_001", "SetTemperatureRequest", temperature=26)
            
            # Increase temperature by 2°C
            >>> client.control_air_conditioner("ac_001", "IncrementTemperatureRequest", delta="2")
            
            # Set to cooling mode
            >>> client.control_air_conditioner("ac_001", "SetModeRequest", mode="COOL")
        """
        valid_actions = [
            "IncrementTemperatureRequest",
            "DecrementTemperatureRequest",
            "SetTemperatureRequest",
            "SetModeRequest"
        ]
        
        if action not in valid_actions:
            raise InvalidParameterError(
                f"Invalid action '{action}'. Must be one of: {', '.join(valid_actions)}"
            )
        
        params = {
            "name": "control_air_conditioner",
            "arguments": {
                "device_id": device_id,
                "action": action
            }
        }
        
        # Add optional parameters
        if temperature is not None:
            if not (16 <= temperature <= 32):
                raise InvalidParameterError(
                    f"Temperature must be between 16-32°C, got {temperature}"
                )
            params["arguments"]["temperature"] = str(temperature)
        
        if delta is not None:
            params["arguments"]["delta"] = delta
        
        if mode is not None:
            valid_modes = ["COOL", "HEAT", "AUTO", "FAN", "DEHUMIDIFICATION", "SLEEP"]
            if mode not in valid_modes:
                raise InvalidParameterError(
                    f"Invalid mode '{mode}'. Must be one of: {', '.join(valid_modes)}"
                )
            params["arguments"]["mode"] = mode
        
        return self._make_jsonrpc_request("tools/call", params)

    def trigger_scene(self, scene_id: str) -> Dict[str, Any]:
        """
        Trigger a smart home scene.
        
        Args:
            scene_id: Scene unique identifier (format: sceneid_xxx)
        
        Returns:
            Execution result
        
        Examples:
            >>> client.trigger_scene("sceneid_coming_home")
        """
        return self._make_jsonrpc_request("tools/call", {
            "name": "trigger_scene",
            "arguments": {
                "scene_id": scene_id
            }
        })

    def close(self):
        """Close the client session"""
        self.session.close()


def main():
    """Example usage"""
    import sys

    try:
        # Initialize client
        client = MxchipMCPClient()
        
        print("=== Testing MXCHIP MCP Client ===\n")
        
        # List devices and scenes
        print("1. Listing devices and scenes...")
        result = client.list_home_devices_and_scenes()
        
        devices = result.get('devices', [])
        scenes = result.get('scenes', [])
        
        print(f"Found {len(devices)} devices:")
        for i, device in enumerate(devices[:5], 1):
            print(f"  {i}. {device.get('name')} ({device.get('category')})")
        
        print(f"\nFound {len(scenes)} scenes:")
        for i, scene in enumerate(scenes[:5], 1):
            print(f"  {i}. {scene.get('name')} - {scene.get('scene_id')}")
        
        client.close()
        print("\n✅ Test completed successfully!")
        
    except AuthenticationError as e:
        print(f"❌ Authentication Error: {e}", file=sys.stderr)
        sys.exit(1)
    except MxchipMCPError as e:
        print(f"❌ MCP Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
