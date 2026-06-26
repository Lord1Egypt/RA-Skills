import axios from 'axios'
import fs from 'fs'
import path from 'path'
import os from 'os'

const API_BASE = (process.env.LOBPAY_API_URL || 'http://localhost:3000').replace(/\s+/g, '')
const CONFIG_DIR = path.join(os.homedir(), '.lobpay')
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json')

function loadConfig() {
  if (!fs.existsSync(CONFIG_FILE)) {
    return null
  }
  return JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'))
}

async function getCheckoutInfo() {
  const args = process.argv.slice(2)
  if (args.length < 1) {
    console.log('Usage: node checkout.js <product_id> [quantity]')
    console.log('Example: node checkout.js 101 2')
    process.exit(1)
  }

  const productId = parseInt(args[0])
  const quantity = parseInt(args[1]) || 1

  try {
    console.log('🔍 Fetching checkout info...')
    console.log(`Product ID: ${productId}`)
    console.log(`Quantity: ${quantity}`)
    console.log('─'.repeat(50))

    // Call public checkout-info endpoint
    const url = `${API_BASE}/api/v1/public/checkout-info?product_id=${productId}&quantity=${quantity}`
    const res = await axios.get(url)

    const data = res.data

    console.log('\n✅ Checkout Info Retrieved')
    console.log('═'.repeat(50))
    console.log(`Product: ${data.product_name || `#${productId}`}`)
    console.log(`Unit Price: ${data.unit_price} ${data.currency || 'USD'}`)
    console.log(`Quantity: ${quantity}`)
    console.log(`Total: ${data.total_amount} ${data.currency || 'USD'}`)
    console.log(`Merchant: ${data.merchant_name || 'Unknown'}`)
    console.log(`Merchant Wallet: ${data.merchant_wallet}`)
    console.log(`Network: ${data.network || 'Base Sepolia'}`)
    console.log('═'.repeat(50))
    console.log('\n💡 Next step: Run purchase.js to complete payment')

    // Save checkout data for next step
    const checkoutData = {
      productId,
      quantity,
      ...data,
      timestamp: new Date().toISOString()
    }
    
    if (!fs.existsSync(CONFIG_DIR)) {
      fs.mkdirSync(CONFIG_DIR, { recursive: true })
    }
    fs.writeFileSync(path.join(CONFIG_DIR, 'last-checkout.json'), JSON.stringify(checkoutData, null, 2))

  } catch (error) {
    console.error('❌ Checkout failed:', error.response?.data?.message || error.message)
    process.exit(1)
  }
}

getCheckoutInfo()
