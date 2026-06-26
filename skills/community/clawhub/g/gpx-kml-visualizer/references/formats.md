# KML / GPX File Format Reference

## KML (Keyhole Markup Language)

KML is an XML-based format for geographic annotation. For track/route visualization, the relevant structure is:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.1">
  <Folder>
    <name>Track Name</name>
    <Placemark>
      <name>Track</name>
      <LineString>
        <coordinates>
          lon1,lat1,ele1 lon2,lat2,ele2 lon3,lat3,ele3 ...
        </coordinates>
      </LineString>
    </Placemark>
  </Folder>
</kml>
```

Key parsing rules:
- The `<coordinates>` element contains space-separated triples: `longitude,latitude,altitude`
- Multiple `<coordinates>` blocks may exist; concatenate all points in document order
- Namespace URI may vary (commonly `http://earth.google.com/kml/2.1` or `http://www.opengis.net/kml/2.2`)

## GPX (GPS Exchange Format)

GPX is an XML schema for GPS data. Track structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<gpx xmlns="http://www.topografix.com/GPX/1/1" creator="..." version="1.1">
  <metadata>...</metadata>
  <trk>
    <name>Track Name</name>
    <type>running</type>
    <trkseg>
      <trkpt lat="31.1873223" lon="119.8048958">
        <ele>87</ele>
        <time>2026-04-18T23:59:47Z</time>
        <extensions>
          <!-- vendor-specific extensions like cadence, hr, speed -->
        </extensions>
      </trkpt>
      ...
    </trkseg>
  </trk>
</gpx>
```

Key parsing rules:
- Track points are `<trkpt>` elements inside `<trkseg>` inside `<trk>`
- Latitude and longitude are attributes: `lat="..." lon="..."`
- Elevation is the `<ele>` child element text content
- Multiple `<trkseg>` segments may exist; concatenate all points
- Namespace URI is typically `http://www.topografix.com/GPX/1/1`
- Extensions under `<extensions>` are vendor-specific and can be ignored for basic visualization
