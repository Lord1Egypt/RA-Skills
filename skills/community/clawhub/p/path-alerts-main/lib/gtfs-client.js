import GtfsRealtimeBindings from 'gtfs-realtime-bindings';

const GTFS_RT_URL = 'https://path.transitdata.nyc/gtfsrt';

// Cache GTFS data for 30 seconds to avoid hammering the server
let cachedFeed = null;
let cacheTime = 0;
const CACHE_TTL = 30000; // 30 seconds

/**
 * Fetch and parse GTFS-RT feed
 */
export async function getGtfsFeed() {
  const now = Date.now();
  
  // Return cached data if still fresh
  if (cachedFeed && (now - cacheTime) < CACHE_TTL) {
    return cachedFeed;
  }
  
  try {
    const response = await fetch(GTFS_RT_URL);
    if (!response.ok) {
      throw new Error(`GTFS-RT fetch failed: ${response.status}`);
    }
    
    const buffer = await response.arrayBuffer();
    const feed = GtfsRealtimeBindings.transit_realtime.FeedMessage.decode(
      new Uint8Array(buffer)
    );
    
    cachedFeed = feed;
    cacheTime = now;
    
    return feed;
  } catch (error) {
    console.error('Failed to fetch GTFS-RT:', error.message);
    return null;
  }
}

/**
 * Get upcoming trains for a specific station
 * Station IDs match GTFS static feed
 */
export async function getTrainsAtStation(stationId) {
  const feed = await getGtfsFeed();
  if (!feed) return [];
  
  const trains = [];
  const now = Math.floor(Date.now() / 1000);
  
  feed.entity.forEach(entity => {
    if (entity.tripUpdate && entity.tripUpdate.stopTimeUpdate) {
      entity.tripUpdate.stopTimeUpdate.forEach(stu => {
        if (stu.stopId === stationId && stu.arrival) {
          const arrivalTime = stu.arrival.time?.toNumber() || 0;
          if (arrivalTime > now) {
            trains.push({
              routeId: entity.tripUpdate.trip?.routeId || 'Unknown',
              tripId: entity.tripUpdate.trip?.tripId,
              arrivalTime: arrivalTime,
              secondsToArrival: arrivalTime - now,
              stopId: stationId
            });
          }
        }
      });
    }
  });
  
  // Sort by arrival time
  return trains.sort((a, b) => a.arrivalTime - b.arrivalTime);
}

/**
 * Format seconds to human-readable time
 */
export function formatWaitTime(seconds) {
  if (seconds < 60) return 'Arriving';
  if (seconds < 120) return '1 min';
  const mins = Math.floor(seconds / 60);
  return `${mins} min`;
}

/**
 * Get formatted arrivals for a station
 */
export async function getArrivalsMessage(stationId, stationName) {
  const trains = await getTrainsAtStation(stationId);
  
  if (trains.length === 0) {
    return `No upcoming trains found for ${stationName}`;
  }
  
  let msg = `🚊 **${stationName}** - Next trains:\n\n`;
  
  // Group by route
  const byRoute = {};
  trains.slice(0, 8).forEach(train => {
    if (!byRoute[train.routeId]) byRoute[train.routeId] = [];
    byRoute[train.routeId].push(train);
  });
  
  Object.entries(byRoute).forEach(([routeId, routeTrains]) => {
    msg += `**${routeId}**: `;
    msg += routeTrains.slice(0, 3).map(t => 
      formatWaitTime(t.secondsToArrival)
    ).join(', ');
    msg += '\n';
  });
  
  return msg;
}

export default {
  getGtfsFeed,
  getTrainsAtStation,
  getArrivalsMessage,
  formatWaitTime
};
