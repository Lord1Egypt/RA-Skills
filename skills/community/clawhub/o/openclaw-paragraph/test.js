#!/usr/bin/env node

/**
 * Basic integration tests for Paragraph OpenClaw skill
 * Run with: npm test
 */

import tools from "./skill.js"

async function runTests() {
  console.log("🧪 Running Paragraph skill tests...\n")
  let passed = 0
  let failed = 0

  // Test 1: Skill loads and has expected number of tools
  try {
    console.log("Test: Skill module loads")
    const toolNames = Object.keys(tools)
    if (toolNames.length >= 15) {
      console.log(`  ✅ Loaded ${toolNames.length} tools`)
      passed++
    } else {
      console.log(`  ❌ Expected at least 15 tools, got ${toolNames.length}`)
      failed++
    }
  } catch (error) {
    console.log(`  ❌ Module load error: ${error.message}`)
    failed++
  }

  // Test 2: Tool signature validation (call without required params should fail gracefully)
  try {
    console.log("\nTest: paragraph_createPost missing params")
    const result = await tools.paragraph_createPost({})
    if (!result.success && result.error.includes("required")) {
      console.log("  ✅ Correctly rejects missing title/markdown")
      passed++
    } else {
      console.log("  ❌ Should have failed with missing params")
      failed++
    }
  } catch (error) {
    console.log(`  ❌ Test error: ${error.message}`)
    failed++
  }

  // Test 3: paragraph_getPost missing ID
  try {
    console.log("\nTest: paragraph_getPost missing postId")
    const result = await tools.paragraph_getPost({})
    if (!result.success && result.error.includes("postId is required")) {
      console.log("  ✅ Correctly rejects missing postId")
      passed++
    } else {
      console.log("  ❌ Should have failed with missing postId")
      failed++
    }
  } catch (error) {
    console.log(`  ❌ Test error: ${error.message}`)
    failed++
  }

  // Test 4: API key check
  try {
    console.log("\nTest: paragraph_testConnection without API key")
    // Temporarily clear env to test error handling
    const originalKey = process.env.PARAGRAPH_API_KEY
    process.env.PARAGRAPH_API_KEY = undefined
    const result = await tools.paragraph_testConnection({})
    if (!result.success && result.error.includes("PARAGRAPH_API_KEY")) {
      console.log("  ✅ Correctly detects missing API key")
      passed++
    } else {
      console.log("  ❌ Should have failed with missing API key")
      failed++
    }
    // Restore
    process.env.PARAGRAPH_API_KEY = originalKey
  } catch (error) {
    console.log(`  ❌ Test error: ${error.message}`)
    failed++
  }

  // Test 5: Connection test with API key (only if set)
  if (process.env.PARAGRAPH_API_KEY) {
    try {
      console.log("\nTest: paragraph_testConnection with API key")
      const result = await tools.paragraph_testConnection({})
      if (result.success && typeof result.data.totalSubscribers === 'number') {
        console.log(`  ✅ Connected! Total subscribers: ${result.data.totalSubscribers}`)
        passed++
      } else {
        console.log(`  ❌ Connection failed: ${result.error}`)
        failed++
      }
    } catch (error) {
      console.log(`  ❌ Test error: ${error.message}`)
      failed++
    }
  } else {
    console.log("\n⚠️  Skipping live connection test (PARAGRAPH_API_KEY not set)")
  }

  console.log(`\n📊 Results: ${passed} passed, ${failed} failed`)
  process.exit(failed > 0 ? 1 : 0)
}

runTests().catch(error => {
  console.error("Fatal test error:", error)
  process.exit(1)
})
