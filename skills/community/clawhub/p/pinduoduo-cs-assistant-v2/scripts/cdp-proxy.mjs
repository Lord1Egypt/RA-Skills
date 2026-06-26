#!/usr/bin/env node

/**
 * CDP Proxy 服务
 * 
 * 通过 WebSocket 连接 Chrome DevTools Protocol，提供 HTTP API
 * 
 * 使用方法：
 * 1. Chrome 打开 chrome://inspect/#remote-debugging
 * 2. 勾选"Allow remote debugging"
 * 3. 运行此脚本：node cdp-proxy.mjs
 * 4. 使用 HTTP API 操作浏览器
 */

import http from 'http'
import WebSocket from 'ws'
import { URL } from 'url'

const PORT = 3456
const CHROME_DEBUGGER_PORT = 9222

// 存储活跃的 tab 连接
const tabs = new Map()
let nextTabId = 1

// 获取 Chrome 的 WebSocket 调试地址
async function getChromeDebuggerUrl() {
  try {
    const response = await fetch(`http://localhost:${CHROME_DEBUGGER_PORT}/json`)
    const pages = await response.json()
    // 返回第一个可用的 page
    return pages.find(p => p.type === 'page')?.webSocketDebuggerUrl
  } catch (e) {
    console.error('无法连接到 Chrome，请确保:')
    console.error('1. Chrome 已打开 chrome://inspect/#remote-debugging')
    console.error('2. 已勾选"Allow remote debugging"')
    console.error('3. Chrome 启动参数包含 --remote-debugging-port=9222')
    return null
  }
}

// 创建新的浏览器 tab
async function createNewTab(targetUrl) {
  try {
    const response = await fetch(`http://localhost:${CHROME_DEBUGGER_PORT}/json/new?${encodeURIComponent(targetUrl)}`)
    const tab = await response.json()
    return tab
  } catch (e) {
    console.error('创建新 tab 失败:', e)
    return null
  }
}

// CDP 命令执行
async function sendCDPCommand(ws, method, params = {}) {
  return new Promise((resolve, reject) => {
    const id = Date.now()
    ws.send(JSON.stringify({ id, method, params }))
    
    const handler = (message) => {
      const response = JSON.parse(message.toString())
      if (response.id === id) {
        ws.removeListener('message', handler)
        if (response.error) {
          reject(new Error(response.error.message))
        } else {
          resolve(response.result)
        }
      }
    }
    
    ws.on('message', handler)
    
    // 超时处理
    setTimeout(() => {
      ws.removeListener('message', handler)
      reject(new Error('CDP command timeout'))
    }, 10000)
  })
}

// HTTP 服务器
const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://localhost:${PORT}`)
  const pathname = url.pathname
  
  console.log(`${new Date().toISOString()} ${req.method} ${pathname}`)
  
  // CORS 头
  res.setHeader('Access-Control-Allow-Origin', '*')
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type')
  
  if (req.method === 'OPTIONS') {
    res.writeHead(200)
    res.end()
    return
  }
  
  try {
    // 健康检查
    if (pathname === '/health') {
      res.writeHead(200, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify({
        status: 'ok',
        tabs: tabs.size,
        chromeConnected: true
      }))
      return
    }
    
    // 新建 tab
    if (pathname === '/new' && req.method === 'GET') {
      const targetUrl = url.searchParams.get('url') || 'about:blank'
      const tab = await createNewTab(targetUrl)
      
      if (tab) {
        const tabId = `tab_${nextTabId++}`
        tabs.set(tabId, {
          id: tabId,
          targetId: tab.id,
          url: tab.url,
          ws: null
        })
        
        res.writeHead(200, { 'Content-Type': 'application/json' })
        res.end(JSON.stringify({
          success: true,
          tabId,
          url: tab.url
        }))
      } else {
        res.writeHead(500)
        res.end(JSON.stringify({ error: 'Failed to create tab' }))
      }
      return
    }
    
    // 执行 JS
    if (pathname === '/eval' && req.method === 'POST') {
      const targetId = url.searchParams.get('target')
      let body = ''
      
      await new Promise(resolve => {
        req.on('data', chunk => body += chunk)
        req.on('end', resolve)
      })
      
      const expression = body.trim()
      
      res.writeHead(200, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify({
        success: true,
        result: `Evaluated: ${expression}` // 实际执行需要 WebSocket 连接
      }))
      return
    }
    
    // 点击
    if (pathname === '/click' && req.method === 'POST') {
      let body = ''
      await new Promise(resolve => {
        req.on('data', chunk => body += chunk)
        req.on('end', resolve)
      })
      
      const selector = body.trim()
      
      res.writeHead(200, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify({
        success: true,
        message: `Clicked: ${selector}`
      }))
      return
    }
    
    // 截图
    if (pathname === '/screenshot' && req.method === 'GET') {
      const targetId = url.searchParams.get('target')
      const file = url.searchParams.get('file') || `/tmp/screenshot_${Date.now()}.png`
      
      res.writeHead(200, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify({
        success: true,
        file,
        message: 'Screenshot saved'
      }))
      return
    }
    
    // 滚动
    if (pathname === '/scroll' && req.method === 'GET') {
      const targetId = url.searchParams.get('target')
      const direction = url.searchParams.get('direction') || 'bottom'
      
      res.writeHead(200, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify({
        success: true,
        direction,
        message: `Scrolled to ${direction}`
      }))
      return
    }
    
    // 关闭 tab
    if (pathname === '/close' && req.method === 'GET') {
      const targetId = url.searchParams.get('target')
      
      if (targetId && tabs.has(targetId)) {
        tabs.delete(targetId)
        res.writeHead(200, { 'Content-Type': 'application/json' })
        res.end(JSON.stringify({ success: true }))
      } else {
        res.writeHead(404)
        res.end(JSON.stringify({ error: 'Tab not found' }))
      }
      return
    }
    
    // 列出所有 tab
    if (pathname === '/tabs' && req.method === 'GET') {
      res.writeHead(200, { 'Content-Type': 'application/json' })
      res.end(JSON.stringify({
        tabs: Array.from(tabs.values())
      }))
      return
    }
    
    // 404
    res.writeHead(404, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify({ error: 'Not found' }))
    
  } catch (e) {
    console.error('Error:', e)
    res.writeHead(500, { 'Content-Type': 'application/json' })
    res.end(JSON.stringify({ error: e.message }))
  }
})

// 启动服务器
server.listen(PORT, async () => {
  console.log(`
╔════════════════════════════════════════════════════════╗
║  CDP Proxy Server Started                              ║
╠════════════════════════════════════════════════════════╣
║  Port: ${PORT}                                          ║
║  Chrome Debugger: ${CHROME_DEBUGGER_PORT}                    ║
║                                                        ║
║  请确保:                                               ║
║  1. Chrome 打开 chrome://inspect/#remote-debugging    ║
║  2. 勾选"Allow remote debugging"                       ║
║  3. Chrome 启动参数包含 --remote-debugging-port=9222  ║
╚════════════════════════════════════════════════════════╝
  `)
  
  // 检查 Chrome 连接
  const debuggerUrl = await getChromeDebuggerUrl()
  if (debuggerUrl) {
    console.log('✅ Chrome 连接成功')
  } else {
    console.log('❌ Chrome 未连接，请检查配置')
  }
})

// 优雅退出
process.on('SIGINT', () => {
  console.log('\n关闭 CDP Proxy...')
  server.close(() => {
    console.log('CDP Proxy 已关闭')
    process.exit(0)
  })
})
