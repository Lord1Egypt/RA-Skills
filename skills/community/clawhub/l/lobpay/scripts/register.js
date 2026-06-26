import axios from 'axios'
import { privateKeyToAccount } from 'viem/accounts'
import { getAddress } from 'viem'
import fs from 'fs'
import path from 'path'
import os from 'os'

const API_BASE = (process.env.LOBPAY_API_URL || 'http://localhost:3000').replace(/\s+/g, '')
const CONFIG_DIR = path.join(os.homedir(), '.lobpay')
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json')

async function register() {
  const args = process.argv.slice(2)
  if (args.length < 4) {
    console.log('Usage: node register.js <agent_name> <wallet_address> <private_key> <api_key>')
    console.log('Example: node register.js "Atla_Agent" 0xAddress 0xPrivateKey ak_live_xxx')
    process.exit(1)
  }

  const [agentName, address, privateKey, apiKey] = args

  // Validate private key
  const account = privateKeyToAccount(privateKey)
  const agentAddress = getAddress(account.address)

  console.log(`🔐 Validated wallet: ${agentAddress}`)

  // Save config
  if (!fs.existsSync(CONFIG_DIR)) {
    fs.mkdirSync(CONFIG_DIR, { recursive: true })
  }

  fs.writeFileSync(CONFIG_FILE, JSON.stringify({
    agentName,
    address: agentAddress.toLowerCase(),
    privateKey,
    apiKey,
    registeredAt: new Date().toISOString()
  }, null, 2))

  console.log('\n✅ Agent registered successfully!')
  console.log('─'.repeat(40))
  console.log(`Name: ${agentName}`)
  console.log(`Address: ${agentAddress}`)
  console.log(`API Key: ${apiKey.slice(0, 20)}...`)
  console.log(`Config: ${CONFIG_FILE}`)
}

register()
