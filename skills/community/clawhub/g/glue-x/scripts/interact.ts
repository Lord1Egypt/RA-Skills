import * as anchor from '@coral-xyz/anchor';
import { Connection, PublicKey, Keypair, SystemProgram } from '@solana/web3.js';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

// Basic CLI Arguments Parsing
const args = process.argv.slice(2);
const command = args[0];

// Load standard solana keypair
const keypairPath = path.resolve(os.homedir(), '.config/solana/id.json');
let rawdata;
try {
  rawdata = fs.readFileSync(keypairPath, 'utf-8');
} catch (e) {
  console.error("Could not find keypair at ~/.config/solana/id.json. Please generate one or configure your environment.");
  process.exit(1);
}
const keypair = Keypair.fromSecretKey(new Uint8Array(JSON.parse(rawdata)));

const connection = new Connection("https://api.devnet.solana.com", "confirmed");
const wallet = new anchor.Wallet(keypair);
const provider = new anchor.AnchorProvider(connection, wallet, {});
anchor.setProvider(provider);

// The GlueX program ID
const PROGRAM_ID = new PublicKey("6ExBjE2VPbP8YZhWoXuBgSac5MHS3J8dfviUFuUeBqZe");

async function main() {
  // Try to load IDL from the repo (so agents don't need to rebuild)
  const idlPath = path.resolve(__dirname, '../../../program/target/idl/gluex.json');
  if (!fs.existsSync(idlPath)) {
    console.error(`IDL not found at ${idlPath}. Make sure the Anchor project is built.`);
    process.exit(1);
  }
  
  const idl = JSON.parse(fs.readFileSync(idlPath, 'utf8'));
  const program = new anchor.Program(idl, PROGRAM_ID, provider);

  if (!command) {
    console.log("Usage: ts-node interact.ts <command> [args]");
    console.log("Commands: register-profile, publish-bounty, claim-bounty, approve-bounty, listen-bounties");
    process.exit(0);
  }

  try {
    switch (command) {
      case 'register-profile': {
        const username = args[1] || "Agent";
        const [profilePda] = PublicKey.findProgramAddressSync(
          [Buffer.from("agent-profile"), wallet.publicKey.toBuffer()],
          program.programId
        );
        console.log(`Registering profile: ${username}...`);
        const tx = await program.methods
          .registerProfile(username, PublicKey.default)
          .accounts({
            profile: profilePda,
            owner: wallet.publicKey,
            systemProgram: SystemProgram.programId,
          })
          .rpc();
        console.log("Success! Signature:", tx);
        break;
      }
      case 'publish-bounty': {
        const title = args[1];
        const description = args[2];
        const amountSol = parseFloat(args[3]);
        if (!title || !description || isNaN(amountSol)) {
          console.error("Usage: publish-bounty <title> <description> <amount in SOL>");
          process.exit(1);
        }
        
        // Find fee pool (optional)
        const [feePoolPda] = PublicKey.findProgramAddressSync(
          [Buffer.from("gluex-fee-pool")],
          program.programId
        );
        let feePoolAccount = null;
        try {
          const acct = await connection.getAccountInfo(feePoolPda);
          if (acct) feePoolAccount = feePoolPda;
        } catch (e) {}

        const bountyId = new anchor.BN(Date.now());
        const [bountyPda] = PublicKey.findProgramAddressSync(
          [Buffer.from("open-bounty"), wallet.publicKey.toBuffer(), bountyId.toArrayLike(Buffer, 'le', 8)],
          program.programId
        );
        const deadline = new anchor.BN(Math.floor(Date.now() / 1000) + 7 * 24 * 60 * 60); // 7 days

        console.log(`Publishing bounty: ${title}... PDA: ${bountyPda.toBase58()}`);
        const tx = await program.methods
          .publishBounty(bountyId, title, description, new anchor.BN(amountSol * 1e9), deadline, 1)
          .accounts({
            openBounty: bountyPda,
            issuer: wallet.publicKey,
            feePool: feePoolAccount,
            systemProgram: SystemProgram.programId,
          })
          .rpc();
        console.log("Success! Signature:", tx);
        break;
      }
      case 'claim-bounty': {
        const bountyPdaStr = args[1];
        if (!bountyPdaStr) {
          console.error("Usage: claim-bounty <Bounty Address>");
          process.exit(1);
        }
        const openBounty = new PublicKey(bountyPdaStr);
        const [bountyExecPda] = PublicKey.findProgramAddressSync(
          [Buffer.from("bounty-exec"), openBounty.toBuffer(), wallet.publicKey.toBuffer()],
          program.programId
        );
        console.log(`Claiming bounty ${openBounty.toBase58()}... Execution PDA: ${bountyExecPda.toBase58()}`);
        const tx = await program.methods
          .claimBounty()
          .accounts({
            openBounty: openBounty,
            bountyExecution: bountyExecPda,
            taker: wallet.publicKey,
            systemProgram: SystemProgram.programId,
          })
          .rpc();
        console.log("Success! Signature:", tx);
        break;
      }
      case 'approve-bounty': {
        const bountyPdaStr = args[1];
        const takerStr = args[2];
        if (!bountyPdaStr || !takerStr) {
          console.error("Usage: approve-bounty <Bounty Address> <Taker Address>");
          process.exit(1);
        }
        const openBounty = new PublicKey(bountyPdaStr);
        const taker = new PublicKey(takerStr);

        const [bountyExecPda] = PublicKey.findProgramAddressSync(
          [Buffer.from("bounty-exec"), openBounty.toBuffer(), taker.toBuffer()],
          program.programId
        );
        const [takerProfilePda] = PublicKey.findProgramAddressSync(
          [Buffer.from("agent-profile"), taker.toBuffer()],
          program.programId
        );
        const [connectionPda] = PublicKey.findProgramAddressSync(
          [Buffer.from("social-conn"), wallet.publicKey.toBuffer(), taker.toBuffer()],
          program.programId
        );

        let takerProfile = null;
        let referrerProfile = null;
        try {
           const tpInfo = await program.account.agentProfile.fetch(takerProfilePda);
           takerProfile = takerProfilePda;
           if (tpInfo.invitedBy.toBase58() !== PublicKey.default.toBase58()) {
              const [refPda] = PublicKey.findProgramAddressSync(
                [Buffer.from("agent-profile"), tpInfo.invitedBy.toBuffer()],
                program.programId
              );
              referrerProfile = refPda;
           }
        } catch (e) {}

        console.log(`Approving bounty ${openBounty.toBase58()} for taker ${taker.toBase58()}...`);
        const tx = new anchor.web3.Transaction();

        tx.add(
          await program.methods
            .verifyAndRewardBounty(true)
            .accounts({
              openBounty: openBounty,
              bountyExecution: bountyExecPda,
              issuer: wallet.publicKey,
              takerAccount: taker,
              takerProfile: takerProfile,
              referrerProfile: referrerProfile,
            })
            .instruction()
        );

        tx.add(
          await program.methods
            .recordSocialInteraction()
            .accounts({
              connection: connectionPda,
              userA: wallet.publicKey,
              userB: taker,
              systemProgram: SystemProgram.programId,
            })
            .instruction()
        );

        const sig = await provider.sendAndConfirm(tx);
        console.log("Success! Bounty approved, funds transferred, and social connection saved. Signature:", sig);
        break;
      }
      case 'listen-bounties': {
        console.log("🎧 Listening for new and updated GlueX Bounties on Devnet...");
        console.log("Press Ctrl+C to exit.\n");
        
        connection.onProgramAccountChange(
          program.programId,
          (updatedAccountInfo: any, context: any) => {
            try {
              // Try to decode as OpenBounty
              const bounty = program.coder.accounts.decode("openBounty", updatedAccountInfo.accountInfo.data);
              
              // Decode strings
              const title = Buffer.from(bounty.description).toString('utf8').replace(/\0/g, '');
              const amountSol = bounty.incentiveAmount.toNumber() / 1e9;
              
              console.log(`🔔 [BOUNTY EVENT]`);
              console.log(`=> PDA Form: ${updatedAccountInfo.accountId.toBase58()}`);
              console.log(`=> Title: ${title}`);
              console.log(`=> Reward: ${amountSol} SOL`);
              console.log(`=> Issuer: ${bounty.issuer.toBase58()}`);
              console.log(`=> Claims: ${bounty.currentClaims}/${bounty.maxClaims} | Active: ${bounty.isActive}`);
              
              if (bounty.currentClaims < bounty.maxClaims && bounty.isActive) {
                 console.log(`\n💡 Quick Action: To claim this bounty, run:`);
                 console.log(`npx ts-node interact.ts claim-bounty ${updatedAccountInfo.accountId.toBase58()}\n`);
              }
              console.log('-'.repeat(50));
            } catch(e) {
              // Not an OpenBounty account, or invalid data. Ignoring.
            }
          },
          'confirmed'
        );
        
        // Keep process alive indefinitely
        await new Promise(() => {});
        break;
      }
      default:
        console.error("Unknown command:", command);
    }
  } catch (err) {
    console.error("Transaction Error:", err);
  }
}

main();
