
const { verify } = require('../engine/verifier');

console.log("--- Running LoR System Test ---");

try {
    // 測試存取根目錄的 SKILL.md
    const status = verify('SKILL.md');
    
    // 模擬驗證失敗情況 (存取不存在的檔案)
    const failStatus = verify('non_existent.js');

    if (status && !failStatus) {
        console.log("✅ LoR System logic passed!");
    } else {
        process.exit(1);
    }
} catch (e) {
    console.error("❌ Test Failed:", e.message);
    process.exit(1);
}
