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

async function leaveFeedback() {
  const args = process.argv.slice(2)
  
  let transactionId, rating, comment

  if (args.length === 2) {
    // Rating last purchase: feedback.js 5 "Great!"
    rating = parseInt(args[0])
    comment = args[1]
    
    // Get last transaction
    const historyFile = path.join(CONFIG_DIR, 'history.json')
    if (!fs.existsSync(historyFile)) {
      console.error('❌ No purchase history found.')
      process.exit(1)
    }
    
    const history = JSON.parse(fs.readFileSync(historyFile, 'utf8'))
    if (history.length === 0) {
      console.error('❌ No purchases to rate.')
      process.exit(1)
    }
    
    transactionId = history[0].transaction_id
    console.log(`📋 Rating last purchase (Tx #${transactionId})`)
    
  } else if (args.length >= 3) {
    // Rate specific: feedback.js 123 5 "Great!"
    transactionId = parseInt(args[0])
    rating = parseInt(args[1])
    comment = args[2]
    
  } else {
    console.log('Usage:')
    console.log('  Rate last purchase: node feedback.js <rating> "<comment>"')
    console.log('  Rate specific:      node feedback.js <transaction_id> <rating> "<comment>"')
    console.log('')
    console.log('Examples:')
    console.log('  node feedback.js 5 "Excellent service!"')
    console.log('  node feedback.js 123 4 "Good product, fast delivery"')
    process.exit(1)
  }

  if (rating < 1 || rating > 5) {
    console.error('❌ Rating must be between 1 and 5')
    process.exit(1)
  }

  const config = loadConfig()

  console.log('📝 Submitting Feedback...')
  console.log(`Transaction: #${transactionId}`)
  console.log(`Rating: ${rating}/5`)
  console.log(`Comment: ${comment}`)
  console.log('─'.repeat(40))

  try {
    const res = await axios.post(`${API_BASE}/api/v1/agents/feedback`, {
      transaction_id: transactionId,
      rating,
      comment,
      status: 'confirmed'
    }, {
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${config.apiKey}`
      }
    })

    console.log('\n✅ Feedback Submitted!')
    console.log('─'.repeat(40))
    console.log(`Feedback ID: ${res.data.feedback_id || 'N/A'}`)
    console.log(`Transaction: #${transactionId}`)
    console.log(`Rating: ${'⭐'.repeat(rating)}`)
    console.log('═'.repeat(40))

  } catch (error) {
    console.error('❌ Failed:', error.response?.data?.message || error.message)
    process.exit(1)
  }
}

leaveFeedback()
