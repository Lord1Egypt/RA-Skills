const { getMbusaDealers } = require('../src/tool.js');

async function runTest() {
    console.log("Testing MBUSA Dealer Skill...");
    console.log("Fetching dealers near 30097 (Johns Creek, GA)...\n");

    try {
        // Call the function with a test zip code
        const resultString = await getMbusaDealers("30097", 0, 10, "mbdealer");
        
        // Parse the result back into an object so we can read it easily in the console
        const result = JSON.parse(resultString);

        if (result.status === "success") {
            console.log(`✅ Success! Found ${result.dealers.length} dealers.`);
            console.log("First dealer found:");
            console.log(result.dealers);
        } else {
            console.log(`❌ Error returned from tool: ${result.message}`);
        }
    } catch (error) {
        console.error("❌ Test script crashed:", error);
    }
}

runTest();
