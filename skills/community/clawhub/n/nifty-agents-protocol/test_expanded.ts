import { generateIdentity, signSVG, verifySVG, transferSVG, canonicalizeSVG, computeHash } from './index.js';

async function runExpandedTests() {
    console.log("--- Starting Expanded NASP Tests ---");

    const artist = generateIdentity();
    const collector = generateIdentity();
    const thief = generateIdentity();

    const originalSVG = `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <rect x="10" y="10" width="80" height="80" fill="blue" />
</svg>`;

    // 1. Test Canonicalization Robustness
    console.log("\n[Test 1] Canonicalization Robustness...");
    const signedSVG = await signSVG(originalSVG, artist);
    
    // Add some random whitespace and change attribute order manually to see if verification still works
    const messySVG = signedSVG
        .replace('<rect x="10" y="10"', '<rect   y="10"  x="10" ')
        .replace('fill="blue"', ' fill = "blue" ');
    
    const v1 = await verifySVG(messySVG);
    console.log("Verification after manual formatting change:", v1.isValid ? "✅ Passed" : "❌ Failed");

    // 2. Test Unauthorized Transfer (Thief tries to transfer)
    console.log("\n[Test 2] Unauthorized Transfer...");
    try {
        // Thief tries to transfer the artist's SVG to themselves
        const stolenSVG = await transferSVG(signedSVG, thief, thief.did);
        const v2 = await verifySVG(stolenSVG);
        console.log("Stolen SVG Verification (should be invalid):", v2.isValid ? "❌ Failed (Should be invalid)" : "✅ Passed (Invalid as expected)");
    } catch (e) {
        console.log("Unauthorized transfer caught error:", (e as Error).message);
    }

    // 3. Test Broken Chain (Corrupting a middle signature)
    console.log("\n[Test 3] Broken Chain Integrity...");
    const transferredToCollector = await transferSVG(signedSVG, artist, collector.did);
    const finalTransfer = await transferSVG(transferredToCollector, collector, thief.did);
    
    // Manually corrupt the artist's initial signature in the metadata
    const metadataMatch = finalTransfer.match(/<metadata>nasp:(.*?)<\/metadata>/);
    if (metadataMatch) {
        const metadataStr = Buffer.from(metadataMatch[1], 'base64').toString();
        const metadata = JSON.parse(metadataStr);
        metadata.signature = metadata.signature.substring(0, 10) + "CORRUPTED" + metadata.signature.substring(20);
        const corruptedMetadataBase64 = Buffer.from(JSON.stringify(metadata)).toString('base64');
        const corruptedSVG = finalTransfer.replace(metadataMatch[1], corruptedMetadataBase64);
        
        try {
            const v3 = await verifySVG(corruptedSVG);
            console.log("Corrupted Chain Verification:", v3.isValid ? "❌ Failed (Should be invalid)" : "✅ Passed (Detected corruption)");
        } catch (e) {
            console.log("Corrupted Chain caught error (Valid detection):", (e as Error).message);
        }
    }

    // 4. Test "Replay" / Identity confusion
    console.log("\n[Test 4] Signature for different content...");
    const anotherSVG = `<svg xmlns="http://www.w3.org/2000/svg"><circle r="10"/></svg>`;
    const signedAnother = await signSVG(anotherSVG, artist);
    
    // Try to swap the metadata from 'anotherSVG' into 'originalSVG'
    const metadataAnother = signedAnother.match(/<metadata>nasp:(.*?)<\/metadata>/)![1];
    const swappedSVG = signedSVG.replace(/<metadata>nasp:(.*?)<\/metadata>/, `<metadata>nasp:${metadataAnother}</metadata>`);
    
    const v4 = await verifySVG(swappedSVG);
    console.log("Swapped Metadata Verification:", v4.isValid ? "❌ Failed (Should be invalid)" : "✅ Passed (Detected hash mismatch)");

    console.log("\n--- Expanded Tests Complete ---");
}

runExpandedTests().catch(console.error);
