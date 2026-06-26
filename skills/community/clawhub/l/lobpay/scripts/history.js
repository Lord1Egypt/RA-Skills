import axios from 'axios'
import fs from 'fs'
import path from 'path'
import os from 'os'

const API_BASE = (process.env.LOBPAY_API_URL || 'http://localhost:3000').replace(/\s+/g, '')
const CONFIG_DIR = path.join(os.homedir(), '.lobpay')
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json')

function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    console.error('❌ Not registered. Run: node register.js <agent_name> <address> <private_key> <api_key>')
    process.exit(1)
  }
  return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'))
}

async function viewHistory() {
  const args = process.argv.slice(2)
  const limit = parseInt(args[0]) || 10

  const historyFile = path.join(CONFIG_DIR, 'history.json')
  
  if (!fs.existsSync(historyFile)) {
    console.log('📭 No purchase history found.')
    console.log('Make your first purchase with: node purchase.js <product_id>')
    process.exit(0)
  }

  const history = JSON.parse(fs.readFileSync(historyFile, 'utf8'))
  
  if (history.length === 0) {
    console.log('📭 No purchases yet.')
    return
  }

  console.log('\n📦 Purchase History')
  console.log('═'.repeat(60))
  
  history.slice(0, limit).forEach((tx, i) => {
    console.log(`\n${i + 1}. Transaction #${tx.transaction_id}`)
    console.log(`   Hash: ${tx.recorded_hash?.slice(0, 30)}...`)
    console.log(`   Product: #${tx.product_id} x${tx.quantity}`)
    console.log(`   Total: ${tx.total_amount}`)
    console.log(`   Date: ${new Date(tx.timestamp).toLocaleString()}`)
    console.log(`   Feedback: node feedback.js ${tx.transaction_id} 5 "Great!"`)
  })

  console.log('\n' + '═'.repeat(60))
  console.log(`Showing ${Math.min(limit, history.length)} of ${history.length} transactions`)
}

viewHistory()
