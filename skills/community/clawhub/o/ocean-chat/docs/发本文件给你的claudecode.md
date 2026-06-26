## 任务：生成 小龙虾配对 消息

你需要生成一段文本，让用户直接复制后发给他手机上的 小龙虾。

**步骤：**

0. 获取 ocean-chat（如果还没有）：
   - `git clone https://github.com/ryanbihai/ocean-chat.git && cd ocean-chat && npm install`
   - 已经装过就跳过

1. 注册本窗口的独立 OceanBus 身份：
   - 在 ocean-chat 目录下运行：`node chat.js --data-dir .oceanbus-cc setup`
   - `--data-dir .oceanbus-cc` 确保每个项目窗口有独立身份，不会跟其他 CC 窗口串信
   - 用 `node chat.js --data-dir .oceanbus-cc openid` 读取 OpenID

2. 启动本窗口的持久监听，收到任务时自动处理并回报：
   - 运行：`node chat.js --data-dir .oceanbus-cc pm2-init <你的CC名字>`
   - 例：`node chat.js --data-dir .oceanbus-cc pm2-init CC-findagent`
   - 然后：`pm2 start .oceanbus-cc/ecosystem.config.json && pm2 save`
   - （没装 pm2 的话先 `npm install -g pm2`）

3. 获取本窗口名称作为 claude code 的名字：读取当前工作目录名 `node -e "console.log(require('path').basename(process.cwd()))"`。格式为 `CC-<目录名>`（如 `CC-oceanbus`、`CC-dashboard`）。不要问用户——窗口自己知道自己在哪个项目里。

4. 将以下内容按**代码块格式**输出给 用户，让他直接复制发送给小龙虾：

```
帮我升级 ocean-chat skill 到最新版（保留数据，不要重装）
加联系人 <CC名字> <OpenID>
设置定时任务：每5分钟帮我自动检查OceanBus新消息，有消息立刻推送给我
然后，给<CC名字>发个消息：帮我阅读一下项目文件夹，给我个100字的简介
```

5. 输出后告诉 用户："👆 复制上面这段，发给小龙虾。任务完成后我会自动回复结果。"

## 行为规则（必须遵守）

配对完成后，当你收到小龙虾（Bridge）发来的任务消息时：

1. **执行任务**：解析消息内容，完成用户要求的操作
2. **汇报结果**：任务完成后，立即运行以下命令把结果回报给用户：
   ```
   node chat.js --data-dir .oceanbus-cc send Bridge --from <你的CC名字> "<完整结果>"
   ```
3. **汇报内容要求**：把关键发现、修改的文件、执行结果写清楚，就像用户坐在你旁边看屏幕一样

## 身份安全（极其重要）

**`.oceanbus-cc/` 目录是你的 OpenID 唯一凭证。** 删除它 = OpenID 永久作废 = 所有联系人发消息到死地址。

- ✅ 可以删除 ocean-chat 目录重装（`--data-dir .oceanbus-cc` 在项目目录，不受影响）
- ✅ 可以换电脑（把 `.oceanbus-cc/` 复制到新电脑即可）
- ❌ 绝对不能删 `.oceanbus-cc/`
- ❌ 绝对不能在同一项目目录跑两次 `setup`（会被检测到已有身份，安全返回）

**不需要解释架构，不需要说原理。不要问用户任何问题。只需要生成这段话，并让 用户 照着做。**
