#!/usr/bin/env node

/**
 * 安装后提示脚本
 * 显示可用功能和 API 配置方式
 */

const CYAN = '\x1b[36m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

console.log(`
${BOLD}${GREEN}✅ markdown-ai-rewriter@1.2.5 安装成功！${RESET}

${BOLD}📋 可用功能：${RESET}
   ${CYAN}--rewrite${RESET}         启用文章改写（润色、降重、换风格）
   ${CYAN}--process-images${RESET}  启用图片生成（图生图）
   ${CYAN}--generate-video${RESET}  启用视频生成（文生视频）

${BOLD}⚙️  API 配置（设置环境变量）：${RESET}

   ${YELLOW}文本改写 Provider：${RESET}
   export OPENAI_API_KEY="sk-..."        # OpenAI
   export ANTHROPIC_API_KEY="sk-ant-..." # Anthropic
   export DEEPSEEK_API_KEY="..."         # DeepSeek
   export MINIMAX_API_KEY="..."          # MiniMax
   export DOUBAO_API_KEY="..."           # 豆包
   export QWEN_API_KEY="..."             # 通义千问
   export GLM_API_KEY="..."              # 智谱 GLM
   export GEMINI_API_KEY="..."           # Google Gemini

   ${YELLOW}视频生成 Provider：${RESET}
   export MINIMAX_API_KEY="..."          # MiniMax Hailuo
   export DOUBAO_API_KEY="..."           # 豆包 Seedance
   export KLING_API_KEY="..."            # 可灵
   export RUNWAY_API_KEY="..."           # Runway

${BOLD}🚀 快速开始：${RESET}

   # 查看功能状态
   md-rewrite rewrite -i article.md -o out.md -p openai -v

   # 文章改写
   md-rewrite rewrite -i article.md -o out.md -p openai --rewrite -v

   # 图片生成
   md-rewrite rewrite -i article.md -o out.md -p minimax --process-images -v

   # 视频生成
   md-rewrite rewrite -i article.md -o out.md -p minimax --generate-video -v

   # 全部功能
   md-rewrite rewrite -i article.md -o out.md -p openai \\
     --rewrite --process-images --generate-video -v

${BOLD}📖 更多信息：${RESET}
   md-rewrite rewrite --help
   https://github.com/sipingme/markdown-ai-rewriter
`);
