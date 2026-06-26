# PC 端 TypeScript 格式示例脚本

## 示例1：发送消息脚本

```typescript
//消息在群聊中发送小表情
import * as dotenv from "dotenv";
import { fileURLToPath } from 'url';
import { dirname, join} from 'path';
import path from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 加载环境变量，指定.env文件路径
dotenv.config({ 
  path: join(__dirname, "../../.env")
});

import {
  createRemotePCService,
  IPCService,
  localPCService,
  PCDevice,
  PCAgent,
} from "../../src";
import { launchMESimple } from "../launch.me.simple";
import { setScreenshotConfig } from "../../src/config";

(async () => {
  let pcService: IPCService = undefined as any;
  if (process.argv.includes("--remote")) {
    pcService = await createRemotePCService("http://localhost:3333");
  } else {
    pcService = localPCService;
  }
   // 第一步：启动ME应用
   console.log("\n=== 第一步：启动ME应用 ===");
   await launchMESimple(pcService);

   console.log("\n=== 第二步：发送消息 ===");
   await jingmeGroupSendEmoji(pcService);
})();

export async function jingmeGroupSendEmoji(pcService: IPCService) {
  // 设置截图模式为窗口模式，精确捕获ME应用窗口
  setScreenshotConfig({ mode: 'window' });

  // 使用PCDevice确保应用正常运行
  console.log("🚀 初始化PC设备...");
  const pcDevice = new PCDevice({
    pcService,
    launchOptions: {
      windowInfo: {  // 使用窗口截图模式，精确捕获ME应用窗口
        appName: "ME",
        restoreMinimized: true,
        onlyForRect: false, // 关键：使用直接窗口截图，而不是显示器截图+裁剪
      },
    },
  });

  try {
    await pcDevice.launch();
    console.log("✅ PC设备启动成功");

    const pcAgent = new PCAgent(pcDevice);

    // 截取当前屏幕
    console.log("📸 截取当前屏幕...");
    
    // 创建截图保存路径并打印
    const screenshotPath = path.join(process.cwd(), `screenshot-${Date.now()}.png`);
    console.log(`💾 截图保存路径: ${screenshotPath}`);
    
    const screenshot = await pcDevice.screenshotBase64();
    console.log(`✅ 截图成功，大小: ${screenshot.length.toLocaleString()} 字符`);

    // 步骤1: 在顶部搜索"daijie27"
    console.log("🔍 步骤1: 搜索群聊'10220534754'");
    await pcAgent.aiAction("点击京ME应用中间顶部的搜索框，如果没有激活再点击一下；输入'10220534754'并按 Enter 键搜索");
    
    // 步骤2: 等待搜索结果加载
    console.log("⏳ 步骤2: 等待搜索结果加载...");
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 步骤3: 打开第一个搜索结果
    console.log("👆 步骤3: 打开第一个搜索结果");
    await pcAgent.aiAction("点击“综合”tab 下搜索结果中含有“10220534754”的会话");
    
    // 步骤4: 等待聊天窗口打开
    console.log("⏳ 步骤4: 等待聊天窗口打开...");
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    // 步骤5: 发送小表情
    console.log("💬 步骤5: 发送小表情");
    await pcAgent.aiTap("点击“请输入消息”上方的表情符号");

    await pcAgent.aiAction("在弹出来的表情弹窗上，点击“默认表情”下方第一个微笑表情");
    await new Promise(resolve => setTimeout(resolve, 1000));
    await pcAgent.aiKeyboardPress("Enter");

    console.log("🎉 京ME发送小表情执行完成！");

  } catch (error) {
    console.error("❌ 京ME发送小表情执行失败:", error);
    throw error;
  }
}
```

## 支持的 PC 操作（TypeScript）

| 方法 | TypeScript 语法 | 说明 |
|------|----------------|------|
| 启动应用 | `await pcDevice.launch()` | 启动应用窗口 |
| AI 操作 | `await pcAgent.aiAction('操作描述')` | AI 操作 |
| AI 输出/查询 | `await pcAgent.aiOutput('查询内容')` | AI 输出/查询 |
| 截图 | `await pcDevice.screenshotBase64()` | 截图 |
| 等待 | `await new Promise(resolve => setTimeout(resolve, ms))` | 等待指定时间 |
