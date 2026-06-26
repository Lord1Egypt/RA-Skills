"use strict";
/**
 * Directions15 API - Calculate routes with distance, duration, tolls, etc.
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getDirections = getDirections;
const axios_1 = __importDefault(require("axios"));
/**
 * Parse coordinates string (lon,lat)
 */
function parseCoordinates(coord) {
    const parts = coord.trim().split(",");
    if (parts.length !== 2)
        return null;
    const lon = parseFloat(parts[0]);
    const lat = parseFloat(parts[1]);
    if (isNaN(lon) || isNaN(lat))
        return null;
    if (lon < -180 || lon > 180 || lat < -90 || lat > 90)
        return null;
    return { lon: parts[0], lat: parts[1] };
}
/**
 * Directions15 API를 호출하여 경로 검색
 */
async function getDirections(params) {
    const url = "https://maps.apigw.ntruss.com/map-direction-15/v1/driving";
    const headers = {
        "x-ncp-apigw-api-key-id": params.apiKeyId,
        "x-ncp-apigw-api-key": params.apiKey,
    };
    // 출발지, 도착지 좌표 파싱
    console.log("\n🔍 [1단계] 좌표 검증\n");
    console.log(`📌 출발지: "${params.start}"`);
    const startCoord = parseCoordinates(params.start);
    if (!startCoord) {
        return {
            success: false,
            start: params.start,
            goal: params.goal,
            distance: 0,
            duration: 0,
            toll_fare: 0,
            taxi_fare: 0,
            fuel_price: 0,
            departure_time: "",
            error: `출발지 좌표 형식 오류: ${params.start}. 경도,위도 형식으로 제공해주세요 (예: 127.0683,37.4979)`,
        };
    }
    console.log(`\n📌 도착지: "${params.goal}"`);
    const goalCoord = parseCoordinates(params.goal);
    if (!goalCoord) {
        return {
            success: false,
            start: params.start,
            goal: params.goal,
            distance: 0,
            duration: 0,
            toll_fare: 0,
            taxi_fare: 0,
            fuel_price: 0,
            departure_time: "",
            error: `도착지 좌표 형식 오류: ${params.goal}. 경도,위도 형식으로 제공해주세요 (예: 126.9034,37.5087)`,
        };
    }
    // 경유지가 있으면 검증
    let waypointsCoord = "";
    if (params.waypoints) {
        console.log(`\n📌 경유지: "${params.waypoints}"`);
        const waypointsList = params.waypoints.split("|");
        const resolvedWaypoints = [];
        for (let i = 0; i < waypointsList.length; i++) {
            const waypoint = waypointsList[i];
            console.log(`  경유지 ${i + 1}: "${waypoint}"`);
            const waypointCoord = parseCoordinates(waypoint);
            if (waypointCoord) {
                resolvedWaypoints.push(`${waypointCoord.lon},${waypointCoord.lat}`);
            }
            else {
                return {
                    success: false,
                    start: params.start,
                    goal: params.goal,
                    distance: 0,
                    duration: 0,
                    toll_fare: 0,
                    taxi_fare: 0,
                    fuel_price: 0,
                    departure_time: "",
                    error: `경유지 ${i + 1} 좌표 형식 오류: ${waypoint}. 경도,위도 형식으로 제공해주세요 (예: 127.0700,37.5650)`,
                };
            }
        }
        waypointsCoord = resolvedWaypoints.join("|");
    }
    // Directions15 API 호출
    console.log("\n🗺️ [2단계] 경로 검색 (Directions15 API)\n");
    const query = {
        start: `${startCoord.lon},${startCoord.lat}`,
        goal: `${goalCoord.lon},${goalCoord.lat}`,
    };
    console.log(`  출발지 좌표: ${query.start}`);
    console.log(`  도착지 좌표: ${query.goal}`);
    if (waypointsCoord) {
        query.waypoints = waypointsCoord;
        console.log(`  경유지 좌표: ${waypointsCoord}`);
    }
    if (params.option) {
        query.option = params.option;
        console.log(`  경로 옵션: ${params.option}`);
    }
    if (params.cartype)
        query.cartype = params.cartype;
    if (params.fueltype)
        query.fueltype = params.fueltype;
    if (params.mileage)
        query.mileage = params.mileage;
    if (params.lang)
        query.lang = params.lang;
    try {
        const response = await axios_1.default.get(url, {
            headers,
            params: query,
        });
        const data = response.data;
        if (data.code !== 0) {
            return {
                success: false,
                start: params.start,
                goal: params.goal,
                distance: 0,
                duration: 0,
                toll_fare: 0,
                taxi_fare: 0,
                fuel_price: 0,
                departure_time: "",
                error: `API 에러: ${data.message}`,
            };
        }
        // traoptimal이 기본값, 없으면 첫번째 옵션 사용
        const optionKey = Object.keys(data.route)[0];
        const routes = data.route[optionKey];
        if (!routes || routes.length === 0) {
            return {
                success: false,
                start: params.start,
                goal: params.goal,
                distance: 0,
                duration: 0,
                toll_fare: 0,
                taxi_fare: 0,
                fuel_price: 0,
                departure_time: "",
                error: "경로 정보 없음",
            };
        }
        const summary = routes[0].summary;
        console.log("\n✅ [3단계] 결과\n");
        return {
            success: true,
            start: params.start,
            goal: params.goal,
            distance: summary.distance,
            duration: summary.duration,
            toll_fare: summary.tollFare,
            taxi_fare: summary.taxiFare,
            fuel_price: summary.fuelPrice,
            departure_time: summary.departureTime,
        };
    }
    catch (error) {
        const axiosError = error;
        return {
            success: false,
            start: params.start,
            goal: params.goal,
            distance: 0,
            duration: 0,
            toll_fare: 0,
            taxi_fare: 0,
            fuel_price: 0,
            departure_time: "",
            error: axiosError.message || "알 수 없는 에러",
        };
    }
}
