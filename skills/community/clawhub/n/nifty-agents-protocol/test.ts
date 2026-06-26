import { generateIdentity, signSVG, verifySVG, transferSVG } from './index.js';

async function runTest() {
    console.log("--- Starting NASP Test ---");

    // 1. Setup Agents
    const artist = generateIdentity();
    const collector = generateIdentity();
    const finalBuyer = generateIdentity();

    console.log(`Artist: ${artist.did}`);
    console.log(`Collector: ${collector.did}`);
    console.log(`Final Buyer: ${finalBuyer.did}`);

    // 2. Artist creates an SVG
    const originalSVG = `<svg width="100" height="100" xmlns="http://www.w3.org/2000/svg">
    <circle cx="50" cy="50" r="40" stroke="green" stroke-width="4" fill="yellow" />
</svg>`;

    console.log("\n[Artist] Signing SVG...");
    const signedSVG = await signSVG(originalSVG, artist);
    
    // 3. Verify original
    console.log("[System] Verifying original signature...");
    const v1 = await verifySVG(signedSVG);
    console.log("Verification:", v1);

    // 4. Transfer to Collector
    console.log(`\n[Artist] Transferring to Collector (${collector.did})...`);
    const transferredSVG1 = await transferSVG(signedSVG, artist, collector.did);
    
    const v2 = await verifySVG(transferredSVG1);
    console.log("Verification after transfer 1:", v2);

    // 5. Transfer to Final Buyer
    console.log(`\n[Collector] Transferring to Final Buyer (${finalBuyer.did})...`);
    const transferredSVG2 = await transferSVG(transferredSVG1, collector, finalBuyer.did);
    
    const v3 = await verifySVG(transferredSVG2);
    console.log("Verification after transfer 2:", v3);

    // 6. Test Tampering
    console.log("\n[Attacker] Tampering with SVG (changing color)...");
    const tamperedSVG = transferredSVG2.replace('fill="yellow"', 'fill="red"');
    try {
        const v4 = await verifySVG(tamperedSVG);
        console.log("Tampered Verification Result (should be invalid):", v4.isValid);
    } catch (e) {
        console.log("Tampered Verification failed as expected (or detected as invalid)");
    }

    console.log("\n--- Test Complete ---");
}

runTest().catch(console.error);
