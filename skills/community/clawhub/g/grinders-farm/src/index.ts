export { GameEngine } from "./game/engine.js";
export { LocalStorage } from "./storage/local-storage.js";
export { createNewFarm, plant, water, harvest, sellAll, nextDay } from "./game/farm.js";
export { CROP_DEFS, getCropDef, getAllCropIds } from "./game/crops.js";
export { renderFarmText } from "./render/text-renderer.js";
export { renderFarmImage } from "./render/image-renderer.js";
export type { FarmState, Plot, CropDef, PlantedCrop, CommandResult, InventoryItem } from "./game/types.js";
export { GrowthStage, coordToLabel, labelToCoord } from "./game/types.js";
