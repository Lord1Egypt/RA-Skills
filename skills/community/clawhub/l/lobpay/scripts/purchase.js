import { x402Client, wrapFetchWithPayment } from '@x402/fetch'
import { registerExactEvmScheme } from '@x402/evm/exact/client'
import { privateKeyToAccount } from 'viem/accounts'
import { getAddress } from 'viem'
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

async function purchase() {
  const args = process.argv.slice(2)
  if (args.length < 1) {
    console.log('Usage: node purchase.js <product_id> [quantity]')
    console.log('Example: node purchase.js 101 2')
    process.exit(1)
  }

  const productId = parseInt(args[0])
  const quantity = parseInt(args[1]) || 1
  const config = loadConfig()

  // Initialize x402 client
  const account = privateKeyToAccount(config.privateKey)
  const agentAddress = getAddress(account.address)

  const client = new x402Client()
  registerExactEvmScheme(client, { signer: account })
  const fetchWithPayment = wrapFetchWithPayment(fetch, client)

  console.log('🛒 Initiating LobPay Purchase...')
  console.log(`Agent: ${agentAddress}`)
  console.log(`Product: #${productId} x${quantity}`)
  console.log(`Network: eip155:84532 (Base Sepolia)`)
  console.log('─'.repeat(50))

  try {
    const response = await fetchWithPayment(`${API_BASE}/api/v1/agents/purchase`, {
      method: 'POST',
      body: JSON.stringify({
        items: [{ product_id: productId, quantity }]
      }),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.apiKey}`
      }
    })

    const body = await response.json()

    console.log('\n✅ Purchase Successful!')
    console.log('═'.repeat(50))
    console.log(`Transaction ID: ${body.transaction_id}`)
    console.log(`Recorded Hash: ${body.recorded_hash}`)
    console.log(`Total Amount: ${body.total_amount}`)
    console.log(`Message: ${body.message}`)
    console.log('═'.repeat(50))

    // Save transaction for feedback
    const txData = {
      transaction_id: body.transaction_id,
      recorded_hash: body.recorded_hash,
      product_id: productId,
      quantity,
      total_amount: body.total_amount,
      timestamp: new Date().toISOString()
    }
    
    let history = []
    const historyFile = path.join(CONFIG_DIR, 'history.json')
    if (fs.existsSync(historyFile)) {
      history = JSON.parse(fs.readFileSync(historyFile, 'utf8'))
    }
    history.unshift(txData)
    fs.writeFileSync(historyFile, JSON.stringify(history.slice(0, 50), null, 2)) // Keep last 50

    console.log('\n💡 To leave feedback:')
    console.log(`node feedback.js ${body.transaction_id} 5 "Great product!"`)

  } catch (error) {
    console.error('\n❌ Purchase failed:', error.message)
    if (error.message.includes('Address "null" is invalid')) {
      console.warn('\n💡 The x402 payTo field may be empty.')
      console.warn('   Run checkout.js first to verify merchant wallet.')
    }
    process.exit(1)
  }
}

purchase()
