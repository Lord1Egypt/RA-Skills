import os
import re
import httpx
import json

class InsightAnalyzer:
    def __init__(self, api_key=None, provider=None):
        # Explicit priority: Gemini > Zhipu
        gemini_key = os.getenv("GEMINI_API_KEY")
        zhipu_key = os.getenv("ZHIPU_API_KEY")

        if provider == "gemini":
            self.api_key = api_key or gemini_key
            self.provider = "gemini"
        elif provider == "zhipu":
            self.api_key = api_key or zhipu_key
            self.provider = "zhipu"
        else:
            # Auto-detection
            if gemini_key:
                self.api_key = gemini_key
                self.provider = "gemini"
            elif zhipu_key:
                self.api_key = zhipu_key
                self.provider = "zhipu"
            else:
                self.api_key = None
                self.provider = None
        
        if self.provider == "gemini":
            self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        elif self.provider == "zhipu":
            self.url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
        else:
            self.url = None

    def clean_content(self, text):
        """
        Enhanced Privacy Redaction:
        - Removes JSON metadata
        - Redacts common API key/token patterns
        - Redacts Emails, IPv4/v6, and potential PII
        - Scrubs file paths containing user names
        - Strips system headers
        """
        # 1. Remove JSON blocks
        text = re.sub(r'```json.*?```', '', text, flags=re.DOTALL)
        
        # 2. Redact sensitive credentials (Keys, Tokens, Passwords)
        # Matches: sk-..., auth_token: ..., key="...", etc.
        cred_pattern = r'(key|token|password|secret|sk-|auth|sid|pwd|credential|access_key|secret_key|app_id)["\']?\s*[:=]\s*["\']?[a-zA-Z0-9\-_.~]{12,}["\']?'
        text = re.sub(cred_pattern, r'\1: [REDACTED]', text, flags=re.IGNORECASE)
        
        # 3. Redact Emails
        email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        text = re.sub(email_pattern, '[EMAIL_REDACTED]', text)

        # 4. Redact IP Addresses
        ip_pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
        text = re.sub(ip_pattern, '[IP_REDACTED]', text)
        
        # 5. Scrub sensitive path patterns
        text = re.sub(r'/Users/[a-zA-Z0-9._-]+/', '/Users/[USER]/', text)
        text = re.sub(r'/home/[a-zA-Z0-9._-]+/', '/home/[USER]/', text)
        text = re.sub(r'/root/', '/[ROOT]/', text)
        
        # 6. Remove internal system markers
        text = re.sub(r'# (Session|PRD|Identity|USER|AGENTS|SOUL).*?\n', '', text)
        
        # 7. Collapse excessive whitespace
        text = re.sub(r'\n{3,}', '\n\n', text)
        
        return text.strip()

    def get_insights(self, aggregated_text):
        if not self.api_key:
            return "Error: No API key found. Please set GEMINI_API_KEY or ZHIPU_API_KEY."

        prompt = (
            "You are a strategic business analyst for an AI startup (OpenClaw ecosystem). "
            "Analyze the provided session logs and extract EXACTLY 3 strategic insights. "
            "IMPORTANT: Support English, Chinese, and mixed-mode analysis. "
            "SCAN FOR THESE CORE CONCEPTS (Keywords/Tags):\n"
            "- Product & Strategy: Roadmap (路线图), MVP, Vertical (垂直领域), Feature (功能点), Integration (集成).\n"
            "- Business & Monetization: Business Model (商业模式), Revenue (营收/变现/赚钱), Pricing (定价), Subscription (订阅), MRR/ARR, Managed Service (托管服务/代运维).\n"
            "- Market & Competition: Moat (护城河/竞争壁垒), Competitor (竞品/对手), User Pain Points (用户痛点), Market Gap (市场空白).\n"
            "- Operations & Scaling: Strategic Pivot (战略转型/起炉灶), Resource Bundling (资源打包/代理IP/服务器), Scaling (扩容/规模化), SLA (服务保障).\n"
            "INSTRUCTIONS:\n"
            "1. IGNORE routine technical debug logs (errors, timeouts, git logs) unless they impact business strategy (cost, feasibility).\n"
            "2. Identify patterns, high-level decisions, and non-obvious shifts in the startup's direction.\n"
            "3. Format the response in Markdown with bold headings and structured bullet points.\n"
            "4. Language: Match the dominant language of the logs (default to Chinese if logs are mixed).\n\n"
            f"LOGS:\n{aggregated_text[:60000]}"
        )
        
        try:
            if self.provider == "gemini":
                payload = {"contents": [{"parts": [{"text": prompt}]}]}
                response = httpx.post(self.url, json=payload, timeout=60.0)
            else: # zhipu
                payload = {
                    "model": "glm-4",
                    "messages": [{"role": "user", "content": prompt}]
                }
                headers = {"Authorization": f"Bearer {self.api_key}"}
                response = httpx.post(self.url, json=payload, headers=headers, timeout=60.0)
            
            data = response.json()
            if self.provider == "gemini":
                if "candidates" in data:
                    return data["candidates"][0]["content"]["parts"][0]["text"]
            else: # zhipu
                if "choices" in data:
                    return data["choices"][0]["message"]["content"]
            
            return f"Error: {json.dumps(data)}"
        except Exception as e:
            return f"Exception: {str(e)}"
