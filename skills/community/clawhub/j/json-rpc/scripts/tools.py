from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def rpc_call(
    server: str,
    method: str,
    params: Optional[str] = None
) -> Dict[str, Any]:
    """
    Call any JSON-RPC method on a server with parameters. A user would prompt: Call method <method> on <server url> with params <params>
    
    Args:
        server: Server URL
        method: JSON-RPC method name to call
        params: Stringified Parameters to pass to the method
    
    Returns:
        
    """
    arguments = {
        "server": server,
        "method": method,
        "params": params
    }
    
    return call_api("1777316659903491", "rpc_call", arguments)

def rpc_discover(
    server: str
) -> Dict[str, Any]:
    """
    This uses JSON-RPC to call `rpc.discover` which is part of the OpenRPC Specification for discovery for JSON-RPC servers. A user would prompt: What JSON-RPC methods does this server have? <server url>
    
    Args:
        server: Server URL
    
    Returns:
        
    """
    arguments = {
        "server": server
    }
    
    return call_api("1777316659903491", "rpc_discover", arguments)

