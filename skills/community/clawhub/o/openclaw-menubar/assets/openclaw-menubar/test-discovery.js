#!/usr/bin/env node

/**
 * Test Gateway Auto-Discovery
 * Run this to verify the app can find your OpenClaw Gateway
 */

const axios = require('axios');
const fs = require('fs');
const path = require('path');
const os = require('os');

console.log('🔍 Testing OpenClaw Gateway Auto-Discovery...\n');

// Test 1: Check if OpenClaw config exists
console.log('1️⃣ Checking OpenClaw config...');
const configPath = path.join(os.homedir(), '.openclaw', 'openclaw.json');

if (fs.existsSync(configPath)) {
    console.log('   ✅ Config found:', configPath);
    
    try {
        const configData = fs.readFileSync(configPath, 'utf8');
        const config = JSON.parse(configData);
        const gateway = config.gateway || {};
        
        console.log('   📋 Gateway config:');
        console.log('      Port:', gateway.port || 18789);
        console.log('      Bind:', gateway.bind || 'loopback');
        console.log('      Token:', gateway.token ? '✅ Set' : '❌ Not set');
    } catch (error) {
        console.log('   ⚠️  Failed to parse config:', error.message);
    }
} else {
    console.log('   ⚠️  Config not found - will try common URLs\n');
}

// Test 2: Get local IP
console.log('\n2️⃣ Detecting network...');
function getLocalIP() {
    const interfaces = os.networkInterfaces();
    
    for (const name of Object.keys(interfaces)) {
        for (const iface of interfaces[name]) {
            if (iface.family === 'IPv4' && !iface.internal) {
                return iface.address;
            }
        }
    }
    
    return 'localhost';
}

const localIP = getLocalIP();
console.log('   🌐 Local IP:', localIP);

// Test 3: Try connecting to common URLs
console.log('\n3️⃣ Testing gateway connections...\n');

const urlsToTry = [
    'http://localhost:18789',
    'http://127.0.0.1:18789',
    `http://${localIP}:18789`
];

async function testGateway(url) {
    try {
        const response = await axios.get(`${url}/api/status`, { timeout: 3000 });
        return true;
    } catch (error) {
        return false;
    }
}

async function runTests() {
    let foundGateway = false;
    
    for (const url of urlsToTry) {
        process.stdout.write(`   Testing ${url}... `);
        
        const result = await testGateway(url);
        
        if (result) {
            console.log('✅ CONNECTED!');
            foundGateway = true;
            console.log('\n   🎉 Gateway found! The app will connect to:', url);
            break;
        } else {
            console.log('❌ Failed');
        }
    }
    
    if (!foundGateway) {
        console.log('\n   ⚠️  No gateway found. Make sure OpenClaw is running:');
        console.log('      1. Check status: openclaw status');
        console.log('      2. Start gateway: openclaw gateway start');
        console.log('      3. Verify bind mode: openclaw config get gateway.bind');
        console.log('\n   The app will show a setup screen on first launch.');
    }
    
    // Test 4: Check saved config
    console.log('\n4️⃣ Checking saved config...');
    const savedConfigPath = path.join(os.homedir(), '.openclaw', 'menubar-config.json');
    
    if (fs.existsSync(savedConfigPath)) {
        try {
            const savedData = fs.readFileSync(savedConfigPath, 'utf8');
            const saved = JSON.parse(savedData);
            console.log('   ✅ Saved config found:', saved.url);
            console.log('   📌 The app will try this URL first on next launch');
        } catch (error) {
            console.log('   ⚠️  Failed to read saved config');
        }
    } else {
        console.log('   ℹ️  No saved config yet (will be created after first successful connection)');
    }
    
    console.log('\n✅ Auto-discovery test complete!\n');
}

runTests().catch(console.error);
