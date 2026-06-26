---
name: kmb-bus-arrival
description: Retrieve real-time KMB bus arrival information. getNextArrivals returns plain text; other tools return JSON.
version: 1.2.1
author: Steven Ho
repository: https://github.com/StevenHo1394/kmb-bus-arrival
tools:
  - name: getRouteDirection
    description: List available travel directions for a KMB route. Returns JSON.
    command: python3 kmb_bus.py getRouteDirection {route}
    inputSchema:
      type: object
      required: [route]
      properties:
        route:
          type: string
    output:
      format: json

  - name: getRouteInfo
    description: Get the list of stops for a route with sequence numbers. Returns JSON.
    command: python3 kmb_bus.py getRouteInfo {route} {direction}
    inputSchema:
      type: object
      required: [route, direction]
      properties:
        route:
          type: string
        direction:
          type: string
          enum: ["outbound", "inbound"]
    output:
      format: json

  - name: getBusStopID
    description: Find bus stop ID(s) by name (Chinese or English). Returns JSON.
    command: python3 kmb_bus.py getBusStopID {name}
    inputSchema:
      type: object
      required: [name]
      properties:
        name:
          type: string
    output:
      format: json

  - name: getNextArrivals
    description: Get the next bus arrival times for a specific route/direction/stop. Returns plain text.
    command: python3 kmb_bus.py getNextArrivals {route} {direction} {stopId}
    inputSchema:
      type: object
      required: [route, direction, stopId]
      properties:
        route:
          type: string
        direction:
          type: string
          enum: ["outbound", "inbound", "auto"]
        stopId:
          type: string
    output:
      format: text

Implementation:

- getNextArrivals output:
  ```
  *Route (To Destination)*

  Stop: *Human Readable Stop Name*

  Next arrivals:
  - HH:MM HKT
  - HH:MM HKT
  ```
  If direction="auto" and the stop is served in both directions, multiple blocks are printed.

- Auto-direction: direction="auto" tries both inbound and outbound; reports whichever has the stop. If both, both are shown.

- Alternate stop ID fallback: If the given stop ID is not found on the route, the skill searches the route's stop list for a stop whose Chinese or English name matches the intended location and uses that stop's ID instead.

- All tools except getNextArrivals return JSON.

- Errors: getNextArrivals prints human-readable messages; other tools return JSON with an `error` field.

version: 1.2.1
changes:
  - Full removal of caching — all API calls are fresh
  - Plain-text errors for getNextArrivals; JSON errors for other tools
  - Auto-direction and alternate stop ID fallback retained
  - Docs aligned with code
