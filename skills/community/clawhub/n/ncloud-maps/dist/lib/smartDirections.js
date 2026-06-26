"use strict";
/**
 * Smart Directions Router
 * Uses Directions5 by default, switches to Directions15 only when waypoints >= 5
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.getSmartDirections = getSmartDirections;
const directions_1 = require("./directions");
const directions5_1 = require("./directions5");
/**
 * Smart routing: defaults to Directions5, uses Directions15 only when waypoints >= 5
 */
async function getSmartDirections(params) {
    // Count waypoints
    const waypointCount = params.waypoints
        ? params.waypoints.split("|").length
        : 0;
    // If 5 or more waypoints, use Directions15; otherwise use Directions5
    const useDirections15 = waypointCount >= 5;
    console.log(`\n📊 경유지 개수: ${waypointCount}개`);
    console.log(`🚀 사용 API: ${useDirections15 ? "Directions15 (15개 경유지 지원)" : "Directions5 (기본값)"}\n`);
    if (useDirections15) {
        return (0, directions_1.getDirections)(params);
    }
    else {
        return (0, directions5_1.getDirections5)(params);
    }
}
