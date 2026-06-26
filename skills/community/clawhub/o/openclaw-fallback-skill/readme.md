安装步骤：
创建技能目录
Copy
mkdir -p ~/.openclaw/skills/openclaw-fallback-skill
cd ~/.openclaw/skills/openclaw-fallback-skill
创建配置文件
Copy
cp config.example.json config.json
# 编辑 config.json，填入你的 API URL 和 Key
安装依赖
Copy
npm install axios
重启 OpenClaw
Copy
systemctl --user restart openclaw  # 如果使用 systemd
# 或直接重启你的 OpenClaw 进程
配置说明：
配置项	说明	示例
apiUrl	云端模型 API 地址	https://api.openai.com/v1/chat/completions
apiKey	API 密钥	sk-xxx
modelName	模型名称	gpt-4, claude-3-opus-20240229
fallbackThreshold	触发阈值（0-1）	0.6
maxRetries	最大重试次数	2
timeout	超时时间（秒）	30
支持的 API 格式：
OpenAI 兼容（包括 DeepSeek、智谱等）
Anthropic Claude
自定义格式（通过修改解析逻辑）
触发 Fallback 的场景：
本地模型置信度低于阈值
响应内容为空或过短
响应包含"不知道"、"无法回答"等关键词
响应过于通用无实质内容
高级配置示例：
Copy
{
  "apiUrl": "https://api.deepseek.com/v1/chat/completions",
  "apiKey": "sk-deepseek-xxx",
  "modelName": "deepseek-chat",
  "fallbackThreshold": 0.5,
  "maxRetries": 3,
  "timeout": 60,
  "enableStreaming": true
}
这个技能会自动监控本地模型的回答质量，当检测到无法合理回答时，会无缝切换到你的云端大模型，确保用户始终获得高质量的响应。