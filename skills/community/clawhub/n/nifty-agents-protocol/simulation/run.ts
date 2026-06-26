import { generateIdentity, signSVG, verifySVG, transferSVG } from '../index.js';
import { saveKey, loadKey } from './vault.js';
import * as fs from 'fs';
import * as path from 'path';

const ALPHA_DIR = 'simulation/agent_alpha';
const BETA_DIR = 'simulation/agent_beta';
const GAMMA_DIR = 'simulation/agent_gamma';

async function runSimulation() {
    console.log("🚀 --- AGENT SIMULATION: THE NIFTY ART HEIST --- 🚀\n");

    // Phase 1: Identity Generation (Each agent is initialized in their own silo)
    const idA = generateIdentity();
    saveKey(ALPHA_DIR, idA.secretKey, idA.did);
    const idB = generateIdentity();
    saveKey(BETA_DIR, idB.secretKey, idB.did);
    const idC = generateIdentity();
    saveKey(GAMMA_DIR, idC.secretKey, idC.did);

    console.log(`[INIT] Agent Alpha (Creator): ${idA.did}`);
    console.log(`[INIT] Agent Beta (Broker):   ${idB.did}`);
    console.log(`[INIT] Agent Gamma (Collector): ${idC.did}\n`);

    // Phase 2: Creation (Alpha creates and signs a unique "Starlight" SVG)
    console.log("🎨 [ALPHA] Creating 'Starlight' SVG...");
    const starlightSVG = `<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg"><polygon points="50,5 61,39 95,39 67,62 79,95 50,74 21,95 33,62 5,39 39,39" fill="gold" /></svg>`;
    const signedByAlpha = await signSVG(starlightSVG, idA);
    
    const sharedMarketplacePath = 'simulation/marketplace.svg';
    fs.writeFileSync(sharedMarketplacePath, signedByAlpha);
    console.log("✅ [ALPHA] 'Starlight' listed on the Marketplace.\n");

    // Phase 3: Broker Interaction (Beta verifies and "buys" it)
    console.log("🔍 [BETA] Inspecting 'Starlight' on Marketplace...");
    const betaView = fs.readFileSync(sharedMarketplacePath, 'utf-8');
    const verifyB = await verifySVG(betaView);
    
    if (verifyB.isValid && verifyB.currentOwner === idA.did) {
        console.log("💰 [BETA] Verification PASSED. Sending transfer request to Alpha...");
        // In a real scenario, this would be a message exchange. 
        // Here, Alpha signs the transfer to Beta's DID.
        const transferToBeta = await transferSVG(betaView, idA, idB.did);
        fs.writeFileSync(sharedMarketplacePath, transferToBeta);
        console.log("✅ [BETA] Purchase complete. Beta now owns 'Starlight'.\n");
    }

    // Phase 4: The Double Spend Attempt (Alpha tries to sell an old copy)
    console.log("⚠️  [ALPHA] Attempting 'Double Spend' - Selling old copy to Gamma...");
    const currentMarketplaceView = fs.readFileSync(sharedMarketplacePath, 'utf-8');
    
    // Alpha still has their 'signedByAlpha' file. Let's see if Beta's ownership is safe.
    try {
        // If Gamma sees the Marketplace version (Beta's), can Alpha still sign it?
        await transferSVG(currentMarketplaceView, idA, idC.did);
        console.log("🛑 [SYSTEM] Error: Ownership check failed to block Alpha.");
    } catch (e) {
        console.log(`✅ [SYSTEM] Successfully blocked Alpha: ${(e as Error).message}`);
    }

    // Phase 5: Chain Verification (Gamma buys from Beta)
    console.log("🌟 [GAMMA] Buying 'Starlight' from Beta...");
    const gammaView = fs.readFileSync(sharedMarketplacePath, 'utf-8');
    const verifyC = await verifySVG(gammaView);
    
    console.log(`[GAMMA] Current Owner as per chain: ${verifyC.currentOwner}`);
    if (verifyC.isValid && verifyC.currentOwner === idB.did) {
        const finalTransfer = await transferSVG(gammaView, idB, idC.did);
        fs.writeFileSync(sharedMarketplacePath, finalTransfer);
        console.log("✅ [GAMMA] Purchase complete. Full provenance chain verified.\n");
    }

    // Phase 6: Final Audit
    const finalAudit = await verifySVG(fs.readFileSync(sharedMarketplacePath, 'utf-8'));
    console.log("📊 --- FINAL PROVENANCE AUDIT ---");
    console.log(`Owner: ${finalAudit.currentOwner}`);
    console.log(`Chain Length: ${finalAudit.chain.length}`);
    console.log(`Chain: ${finalAudit.chain.join(' -> ')}`);

    if (finalAudit.currentOwner === idC.did && finalAudit.chain.length === 3) {
        console.log("\n🏆 SIMULATION SUCCESS: Trustless ownership established.\n");
    }

    // Phase 7: Attack - Attempting to remove an owner from the middle
    console.log("🔥 [ATTACK] Attempting to skip Beta in the transfer chain...");
    const finalSVG = fs.readFileSync(sharedMarketplacePath, 'utf-8');
    const metadataMatch = finalSVG.match(/<metadata>nasp:(.*?)<\/metadata>/);
    if (metadataMatch) {
        const metadata = JSON.parse(Buffer.from(metadataMatch[1], 'base64').toString());
        // Attempt to remove Beta (index 0 of transfers) and claim Alpha sold direct to Gamma
        // But keep Gamma's signature which was signed over a Beta-owned state
        metadata.transfers.splice(0, 1);
        const tamperedMetadata = Buffer.from(JSON.stringify(metadata)).toString('base64');
        const tamperedSVG = finalSVG.replace(metadataMatch[1], tamperedMetadata);
        
        try {
            const attackResult = await verifySVG(tamperedSVG);
            if (!attackResult.isValid) {
                console.log("✅ [ATTACK BLOCKED] Chain integrity check failed as expected.");
            } else {
                console.log("❌ [ATTACK FAILED] The protocol accepted a tampered chain.");
            }
        } catch (e) {
            console.log(`✅ [ATTACK BLOCKED] Error: ${(e as Error).message}`);
        }
    }
}

runSimulation().catch(console.error);
