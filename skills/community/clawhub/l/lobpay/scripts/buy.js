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

async function quickBuy() {
  const args = process.argv.slice(2)
  if (args.length < 1) {
    console.log('Usage: node buy.js <product_id> [quantity]')
    console.log('Example: node buy.js 101 2')
    console.log('')
    console.log('This command:')
    console.log('  1. Gets checkout info')
    console.log('  2. Executes X402 payment')
    console.log('  3. Records transaction')
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

  console.log('🛒 LobPay Quick Buy')
  console.log('═'.repeat(50))
  console.log(`Agent: ${agentAddress}`)
  console.log(`Product: #${productId} x${quantity}`)
  console.log(`Network: eip155:84532 (Base Sepolia)`)
  console.log('─'.repeat(50))

  try {
    // Step 1: Get checkout info first
    console.log('\n1️⃣ Fetching checkout info...')
    const checkoutRes = await fetch(`${API_BASE}/api/v1/public/checkout-info?product_id=${productId}&quantity=${quantity}`)
    
    if (!checkoutRes.ok) {
      throw new Error(`Checkout failed: ${checkoutRes.status}`)
    }
    
    const checkoutData = await checkoutRes.json()
    console.log(`   ✅ ${checkoutData.product_name || `Product #${productId}`}`)
    console.log(`   💰 Total: ${checkoutData.total_amount} ${checkoutData.currency || 'USD'}`)
    console.log(`   🏪 Merchant: ${checkoutData.merchant_name || checkoutData.merchant_wallet?.slice(0, 20)}...`)

    // Step 2: Execute purchase with X402
    console.log('\n2️⃣ Executing X402 payment...')
    const purchaseRes = await fetchWithPayment(`${API_BASE}/api/v1/agents/purchase`, {
      method: 'POST',
      body: JSON.stringify({
        items: [{ product_id: productId, quantity }]
      }),
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.apiKey}`
      }
    })

    const purchaseData = await purchaseRes.json()

    // Step 3: Display success
    console.log('\n✅ Purchase Complete!')
    console.log('═'.repeat(50))
    console.log(`Transaction ID: ${purchaseData.transaction_id}`)
    console.log(`Recorded Hash: ${purchaseData.recorded_hash}`)
    console.log(`Amount Paid: ${purchaseData.total_amount}`)
    console.log('═'.repeat(50))

    // Save to history
    const txData = {
      transaction_id: purchaseData.transaction_id,
      recorded_hash: purchaseData.recorded_hash,
      product_id: productId,
      quantity,
      total_amount: purchaseData.total_amount,
      checkout_data: checkoutData,
      timestamp: new Date().toISOString()
    }
    
    let history = []
    const historyFile = path.join(CONFIG_DIR, 'history.json')
    if (fs.existsSync(historyFile)) {
      history = JSON.parse(fs.readFileSync(historyFile, 'utf8'))
    }
    history.unshift(txData)
    fs.writeFileSync(historyFile, JSON.stringify(history.slice(0, 50), null, 2))

    console.log('\n💡 Next steps:')
    console.log(`   View history:  node history.js`)
    console.log(`   Leave review:  node feedback.js 5 "Great product!"`)

  } catch (error) {
    console.error('\n❌ Purchase failed:', error.message)
    process.exit(1)
  }
}

quickBuy()
