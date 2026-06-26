const { encodeFunctionData } = require('viem');

const DIAMOND_ADDRESS = '0xA99c4B08201F2913Db8D28e71d020c4298F29dBF';
const CHAIN_ID = 8453; // Base mainnet
const SLOT_NAMES = ['body', 'face', 'eyes', 'head', 'left-hand', 'right-hand', 'pet', 'background'];

// ABI for equipWearables
const EQUIP_ABI = {
  name: 'equipWearables',
  type: 'function',
  stateMutability: 'nonpayable',
  inputs: [
    { name: '_tokenId', type: 'uint256' },
    { name: '_wearablesToEquip', type: 'uint16[16]' }
  ],
  outputs: []
};

function normalizeGotchiId(gotchiId) {
  const idStr = String(gotchiId);
  if (!/^\d+$/.test(idStr)) {
    throw new Error(`Invalid gotchi ID: ${gotchiId}`);
  }
  return BigInt(idStr);
}

function normalizeWearableId(value, slotName) {
  const id = Number(value);
  if (!Number.isInteger(id) || id < 0 || id > 65535) {
    throw new Error(`Invalid wearable ID for slot ${slotName}: ${value}`);
  }
  return id;
}

function normalizeCurrentWearables(currentWearables) {
  if (currentWearables === null || currentWearables === undefined) {
    return new Array(16).fill(0);
  }

  if (!Array.isArray(currentWearables)) {
    throw new Error('Current wearables must be an array');
  }

  const base = currentWearables.slice(0, 16);
  while (base.length < 16) {
    base.push(0);
  }

  return base.map((value, index) => normalizeWearableId(value, `index-${index}`));
}

/**
 * Build equip transaction.
 *
 * IMPORTANT:
 * equipWearables expects the full 16-slot loadout. If currentWearables
 * is provided, only specified slots are updated and all others are preserved.
 *
 * @param {number|string} gotchiId - Gotchi token ID
 * @param {Object} wearables - Wearable updates { slotName: wearableId }
 * @param {Array<number>} [currentWearables] - Existing 16-slot wearables array
 * @returns {Object} Transaction object for Bankr
 */
function buildEquipTransaction(gotchiId, wearables, currentWearables) {
  const normalizedGotchiId = normalizeGotchiId(gotchiId);

  if (!wearables || typeof wearables !== 'object' || Array.isArray(wearables)) {
    throw new Error('Wearables must be an object: { slotName: wearableId }');
  }

  const slots = normalizeCurrentWearables(currentWearables);

  for (const [slotNameRaw, wearableIdRaw] of Object.entries(wearables)) {
    const slotName = String(slotNameRaw).toLowerCase();
    const slotIndex = SLOT_NAMES.indexOf(slotName);

    if (slotIndex === -1) {
      throw new Error(`Invalid slot name: ${slotNameRaw}. Valid slots: ${SLOT_NAMES.join(', ')}`);
    }

    slots[slotIndex] = normalizeWearableId(wearableIdRaw, slotName);
  }

  const calldata = encodeFunctionData({
    abi: [EQUIP_ABI],
    functionName: 'equipWearables',
    args: [normalizedGotchiId, slots]
  });

  return {
    transaction: {
      to: DIAMOND_ADDRESS,
      chainId: CHAIN_ID,
      value: '0',
      data: calldata
    },
    description: `Equip wearables on Gotchi #${gotchiId}`,
    waitForConfirmation: true
  };
}

/**
 * Build unequip-all transaction
 * @param {number|string} gotchiId - Gotchi token ID
 * @returns {Object} Transaction object for Bankr
 */
function buildUnequipAllTransaction(gotchiId) {
  const normalizedGotchiId = normalizeGotchiId(gotchiId);
  const slots = new Array(16).fill(0);

  const calldata = encodeFunctionData({
    abi: [EQUIP_ABI],
    functionName: 'equipWearables',
    args: [normalizedGotchiId, slots]
  });

  return {
    transaction: {
      to: DIAMOND_ADDRESS,
      chainId: CHAIN_ID,
      value: '0',
      data: calldata
    },
    description: `Unequip all wearables from Gotchi #${gotchiId}`,
    waitForConfirmation: true
  };
}

module.exports = {
  DIAMOND_ADDRESS,
  CHAIN_ID,
  SLOT_NAMES,
  buildEquipTransaction,
  buildUnequipAllTransaction
};
