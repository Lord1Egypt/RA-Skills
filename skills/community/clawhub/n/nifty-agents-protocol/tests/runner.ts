export function expect(condition: boolean, message: string) {
    if (!condition) {
        throw new Error(`❌ FAILED: ${message}`);
    }
}

export async function test(name: string, fn: () => Promise<void>) {
    try {
        console.log(`[TEST] ${name}...`);
        await fn();
        console.log(`✅ PASSED: ${name}`);
        return true;
    } catch (e) {
        console.log((e as Error).message);
        return false;
    }
}

export function summarize(results: boolean[]) {
    const passed = results.filter(r => r).length;
    const total = results.length;
    console.log(`\n📊 --- TEST SUMMARY --- 📊`);
    console.log(`Passed: ${passed} / ${total}`);
    if (passed === total) {
        console.log("🏆 ALL TESTS PASSED! 🏆\n");
    } else {
        console.log(`⚠️  ${total - passed} TESTS FAILED. Check logs above. ⚠️\n`);
        process.exit(1);
    }
}
