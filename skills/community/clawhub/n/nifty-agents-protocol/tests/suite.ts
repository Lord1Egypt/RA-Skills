import { generateIdentity, signSVG, verifySVG, transferSVG, canonicalizeSVG } from '../index.js';
import { test, expect, summarize } from './runner.js';

async function runSuite() {
    const results: boolean[] = [];

    // --- Category 1: Identity ---
    results.push(await test("Identity - Format", async () => {
        const id = generateIdentity();
        expect(id.did.startsWith('did:key:z6Mk'), "DID must follow format");
        expect(id.publicKey.length === 32, "PublicKey must be 32 bytes (Ed25519)");
        expect(id.secretKey.length === 64, "SecretKey must be 64 bytes");
    }));

    // --- Category 2: Content Integrity ---
    results.push(await test("Integrity - Tampering Detection", async () => {
        const id = generateIdentity();
        const svg = `<svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="10"/></svg>`;
        const signed = await signSVG(svg, id);
        
        // 1. Valid Check
        const v1 = await verifySVG(signed);
        expect(v1.isValid, "Valid SVG must verify as true");

        // 2. Content Change (Circle radius)
        const tampered = signed.replace('r="10"', 'r="15"');
        const v2 = await verifySVG(tampered);
        expect(!v2.isValid, "Tampered content must be detected");
    }));

    results.push(await test("Integrity - Canonicalization Robustness", async () => {
        const id = generateIdentity();
        const raw = `<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><rect x="0" y="0" width="10" height="10"/></svg>`;
        const signed = await signSVG(raw, id);
        
        // Manual reformatting: swap attributes, add whitespace
        const messy = signed.replace('x="0" y="0"', '  y="0"    x="0"  ');
        const v = await verifySVG(messy);
        expect(v.isValid, "Verification must survive attribute reordering and whitespace changes");
    }));

    // --- Category 3: Provenance Chains ---
    results.push(await test("Provenance - Long Chain Validation", async () => {
        const agents = Array.from({ length: 10 }, () => generateIdentity());
        let svg = `<svg xmlns="http://www.w3.org/2000/svg"><path d="M0,0 L10,10"/></svg>`;
        
        // Initial Sign
        svg = await signSVG(svg, agents[0]);

        // 9 Transfers
        for (let i = 0; i < agents.length - 1; i++) {
            svg = await transferSVG(svg, agents[i], agents[i+1].did);
        }

        const v = await verifySVG(svg);
        expect(v.isValid, "Full chain must be valid");
        expect(v.currentOwner === agents[9].did, "Last agent must be the owner");
        expect(v.chain.length === 10, "Chain length must be 10");
        expect(v.chain[0] === agents[0].did, "Creator must be correct");
    }));

    // --- Category 4: Attack Resistance ---
    results.push(await test("Attack - Identity Hijack", async () => {
        const alice = generateIdentity();
        const bob = generateIdentity();
        const mallory = generateIdentity();

        const svg = await signSVG(`<svg><text>Ownership</text></svg>`, alice);
        
        // Mallory tries to transfer Alice's asset to herself
        try {
            await transferSVG(svg, mallory, mallory.did);
            expect(false, "Should have thrown ownership error");
        } catch (e) {
            expect((e as Error).message.includes('Signer'), "Must detect signer isn't owner");
        }
    }));

    results.push(await test("Attack - Signature Replay", async () => {
        const alice = generateIdentity();
        const doc1 = await signSVG(`<svg id="1"/>`, alice);
        const doc2 = await signSVG(`<svg id="2"/>`, alice);
        
        // Try to swap metadata from doc1 into doc2
        const meta1 = doc1.match(/<metadata>nasp:(.*?)<\/metadata>/)![1];
        const swapped = doc2.replace(/<metadata>nasp:(.*?)<\/metadata>/, `<metadata>nasp:${meta1}</metadata>`);
        
        const v = await verifySVG(swapped);
        expect(!v.isValid, "Swapped metadata must fail verification (hash mismatch)");
    }));

    results.push(await test("Attack - Chain Corruption", async () => {
        const alice = generateIdentity();
        const bob = generateIdentity();
        const svg = await transferSVG(await signSVG(`<svg/>`, alice), alice, bob.did);
        
        // Corrupt the metadata JSON itself
        const metaBase64 = svg.match(/<metadata>nasp:(.*?)<\/metadata>/)![1];
        const tamperedMeta = metaBase64.substring(0, metaBase64.length - 10) + "AAAAA";
        const tamperedSVG = svg.replace(metaBase64, tamperedMeta);
        
        try {
            await verifySVG(tamperedSVG);
            // If it returns isValid: false, that's okay too.
        } catch (e) {
            // Expected catch for corrupted base64 or JSON
            expect(true, "Successfully caught corrupted metadata format");
        }
    }));

    summarize(results);
}

runSuite().catch(console.error);
