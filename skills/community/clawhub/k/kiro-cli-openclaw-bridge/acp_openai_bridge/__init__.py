"""ACP-to-OpenAI Bridge

A local HTTP proxy service that translates OpenAI-compatible requests
into ACP (Agent Client Protocol) JSON-RPC 2.0 calls, communicating with
kiro-cli acp via stdio pipes.
"""

__version__ = "1.0.0"
