const { ethers } = require('ethers');
const fs = require('fs');
const path = require('path');

const AAVEGOTCHI_DIAMOND = '0xA99c4B08201F2913Db8D28e71d020c4298F29dBF';
const BASE_RPC = process.env.BASE_MAINNET_RPC || 'https://mainnet.base.org';

const ABI = [
  'function getAavegotchiSvg(uint256 _tokenId) external view returns (string memory)',
  'function getAavegotchi(uint256 _tokenId) external view returns (tuple(uint256 tokenId, string name, address owner, uint256 randomNumber, uint256 status, int16[6] numericTraits, int16[6] modifiedNumericTraits, uint16[16] equippedWearables, address collateral, address escrow, uint256 stakedAmount, uint256 minimumStake, uint256 kinship, uint256 lastInteracted, uint256 experience, uint256 toNextLevel, uint256 usedSkillPoints, uint256 level, uint256 hauntId, uint256 baseRarityScore, uint256 modifiedRarityScore, bool locked))'
];

const STATUS_NAMES = {
  0: 'Portal (Unopened)',
  1: 'Portal (Opened)',
  2: 'Gotchi',
  3: 'Gotchi'
};

function toNum(v) {
  return Number(v.toString());
}

async function fetchGotchi(tokenId, outputDir = '.') {
  if (!Number.isInteger(tokenId) || tokenId < 0) {
    throw new Error(`Invalid tokenId: ${tokenId}`);
  }

  fs.mkdirSync(outputDir, { recursive: true });

  const provider = new ethers.JsonRpcProvider(BASE_RPC);
  const contract = new ethers.Contract(AAVEGOTCHI_DIAMOND, ABI, provider);

  try {
    console.log(`\n🔍 Fetching Gotchi #${tokenId} from Base mainnet...`);

    const gotchiData = await contract.getAavegotchi(tokenId);
    const status = toNum(gotchiData.status);
    const statusName = STATUS_NAMES[status] || `Unknown (${status})`;

    const baseBrsNum = toNum(gotchiData.baseRarityScore);
    const totalBrsNum = toNum(gotchiData.modifiedRarityScore);
    const wearablesMod = totalBrsNum - baseBrsNum;

    const equippedWearables = gotchiData.equippedWearables
      .map((w) => toNum(w))
      .filter((w) => w > 0)
      .map((w) => w.toString());

    const result = {
      tokenId: tokenId.toString(),
      name: gotchiData.name || 'Unnamed',
      owner: gotchiData.owner,
      status,
      statusName,
      hauntId: gotchiData.hauntId.toString(),
      baseRarityScore: gotchiData.baseRarityScore.toString(),
      modifiedRarityScore: gotchiData.modifiedRarityScore.toString(),
      brs: gotchiData.modifiedRarityScore.toString(),
      baseBrs: gotchiData.baseRarityScore.toString(),
      wearablesModifier: wearablesMod.toString(),
      kinship: gotchiData.kinship.toString(),
      level: gotchiData.level.toString(),
      experience: gotchiData.experience.toString(),
      collateral: gotchiData.collateral,
      stakedAmount: ethers.formatEther(gotchiData.stakedAmount),
      locked: gotchiData.locked,
      equippedWearables,

      traits: {
        energy: gotchiData.numericTraits[0].toString(),
        aggression: gotchiData.numericTraits[1].toString(),
        spookiness: gotchiData.numericTraits[2].toString(),
        brainSize: gotchiData.numericTraits[3].toString(),
        eyeShape: gotchiData.numericTraits[4].toString(),
        eyeColor: gotchiData.numericTraits[5].toString()
      },

      modifiedTraits: {
        energy: gotchiData.modifiedNumericTraits[0].toString(),
        aggression: gotchiData.modifiedNumericTraits[1].toString(),
        spookiness: gotchiData.modifiedNumericTraits[2].toString(),
        brainSize: gotchiData.modifiedNumericTraits[3].toString(),
        eyeShape: gotchiData.modifiedNumericTraits[4].toString(),
        eyeColor: gotchiData.modifiedNumericTraits[5].toString()
      }
    };

    if (status === 2 || status === 3) {
      console.log(`📛 Name: ${result.name}`);
      console.log(`⭐ Total BRS: ${result.brs} (Base: ${result.baseBrs} + Wearables: ${wearablesMod >= 0 ? '+' : ''}${wearablesMod})`);
      console.log(`💜 Kinship: ${result.kinship}`);
      console.log(`🎯 Level: ${result.level}`);
      console.log(`✨ XP: ${result.experience}`);
      console.log(`🔒 Locked: ${result.locked ? 'Yes' : 'No'}`);
      console.log(`\n🎭 Base Traits (without wearables):`);
      console.log(`   Energy: ${result.traits.energy}`);
      console.log(`   Aggression: ${result.traits.aggression}`);
      console.log(`   Spookiness: ${result.traits.spookiness}`);
      console.log(`   Brain Size: ${result.traits.brainSize}`);
      console.log(`\n👔 Modified Traits (with wearables):`);
      console.log(`   Energy: ${result.modifiedTraits.energy} (${toNum(result.modifiedTraits.energy) - toNum(result.traits.energy) >= 0 ? '+' : ''}${toNum(result.modifiedTraits.energy) - toNum(result.traits.energy)})`);
      console.log(`   Aggression: ${result.modifiedTraits.aggression} (${toNum(result.modifiedTraits.aggression) - toNum(result.traits.aggression) >= 0 ? '+' : ''}${toNum(result.modifiedTraits.aggression) - toNum(result.traits.aggression)})`);
      console.log(`   Spookiness: ${result.modifiedTraits.spookiness} (${toNum(result.modifiedTraits.spookiness) - toNum(result.traits.spookiness) >= 0 ? '+' : ''}${toNum(result.modifiedTraits.spookiness) - toNum(result.traits.spookiness)})`);
      console.log(`   Brain Size: ${result.modifiedTraits.brainSize} (${toNum(result.modifiedTraits.brainSize) - toNum(result.traits.brainSize) >= 0 ? '+' : ''}${toNum(result.modifiedTraits.brainSize) - toNum(result.traits.brainSize)})`);
    }

    console.log(`\n📥 Fetching SVG...`);
    const svg = await contract.getAavegotchiSvg(tokenId);

    let imageType = 'Unknown';
    if (svg.includes('gotchi-body') || svg.includes('gotchi-wearable')) {
      imageType = 'Aavegotchi';
    } else if (svg.includes('Haunt')) {
      imageType = 'Portal';
    }
    result.imageType = imageType;

    const jsonPath = path.join(outputDir, `gotchi-${tokenId}.json`);
    fs.writeFileSync(jsonPath, JSON.stringify(result, null, 2));
    console.log(`\n✅ Saved JSON: ${jsonPath}`);

    const svgPath = path.join(outputDir, `gotchi-${tokenId}.svg`);
    fs.writeFileSync(svgPath, svg);
    console.log(`✅ Saved SVG: ${svgPath} (${imageType})`);

    return result;
  } catch (error) {
    if ((error.message || '').includes('SVG type or id does not exist')) {
      console.error(`\n❌ Gotchi #${tokenId} does not exist on Base chain`);
      console.error('Fatal error:', error.message);
      process.exit(1);
    }
    throw error;
  }
}

if (require.main === module) {
  const rawTokenId = process.argv[2];
  const outputDir = process.argv[3] || '.';

  if (!rawTokenId || !/^\d+$/.test(rawTokenId)) {
    console.error('Usage: node fetch-gotchi.js <tokenId> [outputDir]');
    process.exit(1);
  }

  fetchGotchi(Number.parseInt(rawTokenId, 10), outputDir)
    .then(() => process.exit(0))
    .catch((error) => {
      console.error('Error:', error);
      process.exit(1);
    });
}

module.exports = { fetchGotchi };
