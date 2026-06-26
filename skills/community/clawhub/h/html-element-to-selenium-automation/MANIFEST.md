# html-to-selenium Skill Manifest

name: html-to-selenium
version: 2.0.5
description:
  将任意网页转换为可运行的 Python Selenium 自动化脚本。
  流程：Playwright 抓取页面 → AI 分析 DOM → 生成 Selenium 代码 + 操作步骤。
  支持：公开页面、登录拦截页面、表单填写、真实用户点击、步骤记录。
  触发词：分析页面、生成 selenium、网页自动化、帮我操作 xxx。
  凭据来源：环境变量 ROUTER_USERNAME / ROUTER_PASSWORD 或命令行参数，对话中提供。
  安全提示：仅用于可信内网设备；优先使用最小权限账户；勿在公共网络传发明文凭据。
  不支持：复杂验证码（滑块/点选）和 MFA。

runtime:
  requires:
    - python3
    - playwright
    - selenium
    - webdriver (Chrome/Chromium)
  install: |
    pip install playwright selenium
    playwright install chromium

env:
  - name: ROUTER_USERNAME
    description: 自动登录用户名（可选）/ Username for auto-login (optional)
  - name: ROUTER_PASSWORD
    description: 自动登录密码（可选）/ Password for auto-login (optional)
  - name: ROUTER_USER
    description: 用户名别名（同 ROUTER_USERNAME）/ Alias for ROUTER_USERNAME
  - name: ROUTER_PASS
    description: 密码别名（同 ROUTER_PASSWORD）/ Alias for ROUTER_PASSWORD

security:
  credential_handling: env_only
  autonomous: true
  disclaimer: |
    注意：本 Skill 可能使用提供的凭据执行自动登录。
    请仅使用可信账户，切勿在公共网络上传输明文凭据。
    WARNING: This skill may perform automated logins using provided credentials.
    Only use trusted accounts. Do not transmit plaintext credentials over public networks.

note: |
  fetch_page.py 会读取 ROUTER_USERNAME / ROUTER_PASSWORD（或别名 ROUTER_USER / ROUTER_PASS）
  环境变量优先；未设置时凭据由用户在对话中提供。
  不主动提取或传输 Cookie / Session，仅当页面 DOM 显式暴露时由 AI 在分析阶段提取。
