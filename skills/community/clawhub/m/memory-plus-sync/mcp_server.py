#!/usr/bin/env python3
"""
Memory-Plus MCP 服务器
提供标准 MCP 接口，与 OpenClaw 集成
"""

import asyncio
import json
import logging
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from mcp.server import Server, NotificationOptions
from mcp.server.models import InitializationOptions
import mcp.server.stdio
import mcp.types as types

from core.main_integration import memory_plus_integration
from core.config_manager import config_manager

logger = logging.getLogger(__name__)

class MemoryPlusMCPServer:
    """Memory-Plus MCP 服务器"""
    
    def __init__(self):
        self.server = Server("memory-plus")
        self.setup_handlers()
        
        logger.info("✅ Memory-Plus MCP 服务器初始化完成")
    
    def setup_handlers(self):
        """设置 MCP 处理器"""
        
        @self.server.list_tools()
        async def handle_list_tools() -> List[types.Tool]:
            """列出可用工具"""
            return [
                types.Tool(
                    name="memory_plus_process",
                    description="处理并存储记忆到 Memory-Plus 系统",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "content": {
                                "type": "string",
                                "description": "记忆内容"
                            },
                            "metadata": {
                                "type": "object",
                                "description": "附加元数据",
                                "additionalProperties": True
                            }
                        },
                        "required": ["content"]
                    }
                ),
                types.Tool(
                    name="memory_plus_get_stats",
                    description="获取 Memory-Plus 系统统计信息",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="memory_plus_test_connection",
                    description="测试模型连接",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                types.Tool(
                    name="memory_plus_reset_stats",
                    description="重置统计信息",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def handle_call_tool(
            name: str,
            arguments: Optional[Dict[str, Any]] = None
        ) -> List[types.TextContent]:
            """调用工具"""
            arguments = arguments or {}
            
            try:
                if name == "memory_plus_process":
                    content = arguments.get("content", "")
                    metadata = arguments.get("metadata", {})
                    
                    if not content:
                        return [types.TextContent(
                            type="text",
                            text="错误：记忆内容不能为空"
                        )]
                    
                    # 处理记忆
                    result = await memory_plus_integration.process_and_store_memory(content, metadata)
                    
                    response_text = json.dumps(result, indent=2, ensure_ascii=False)
                    return [types.TextContent(
                        type="text",
                        text=f"记忆处理完成:\n{response_text}"
                    )]
                
                elif name == "memory_plus_get_stats":
                    stats = memory_plus_integration.get_stats()
                    response_text = json.dumps(stats, indent=2, ensure_ascii=False)
                    return [types.TextContent(
                        type="text",
                        text=f"系统统计:\n{response_text}"
                    )]
                
                elif name == "memory_plus_test_connection":
                    result = config_manager.test_connection()
                    return [types.TextContent(
                        type="text",
                        text=f"连接测试: {result['success']} - {result['message']}"
                    )]
                
                elif name == "memory_plus_reset_stats":
                    memory_plus_integration.reset_stats()
                    return [types.TextContent(
                        type="text",
                        text="统计信息已重置"
                    )]
                
                else:
                    return [types.TextContent(
                        type="text",
                        text=f"未知工具: {name}"
                    )]
                    
            except Exception as e:
                logger.error(f"调用工具失败: {e}")
                return [types.TextContent(
                    type="text",
                    text=f"工具调用失败: {str(e)}"
                )]
        
        @self.server.list_resources()
        async def handle_list_resources() -> List[types.Resource]:
            """列出可用资源"""
            return [
                types.Resource(
                    uri="memory-plus://config",
                    name="Memory-Plus 配置",
                    description="Memory-Plus 系统配置",
                    mimeType="application/json"
                ),
                types.Resource(
                    uri="memory-plus://stats",
                    name="Memory-Plus 统计",
                    description="系统运行统计信息",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def handle_read_resource(uri: str) -> str:
            """读取资源"""
            if uri == "memory-plus://config":
                settings = config_manager.load_settings()
                return json.dumps(settings, indent=2, ensure_ascii=False)
            elif uri == "memory-plus://stats":
                stats = memory_plus_integration.get_stats()
                return json.dumps(stats, indent=2, ensure_ascii=False)
            else:
                return f"未知资源: {uri}"
    
    async def run(self):
        """运行 MCP 服务器"""
        async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                InitializationOptions(
                    server_name="memory-plus",
                    server_version="1.0.0",
                    capabilities=self.server.get_capabilities(
                        notification_options=NotificationOptions(),
                        experimental_capabilities={},
                    ),
                )
            )

async def main():
    """主函数"""
    # 配置日志
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger.info("🚀 启动 Memory-Plus MCP 服务器...")
    
    # 创建并运行服务器
    server = MemoryPlusMCPServer()
    await server.run()

if __name__ == "__main__":
    asyncio.run(main())
