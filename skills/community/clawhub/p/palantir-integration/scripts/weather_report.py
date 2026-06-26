import argparse
from mss_client import api_get


def weather_report(lat, lon, hours):
    data = api_get("/weather", params={"lat": lat, "lon": lon, "forecast_hours": hours})
    current = data["current"]

    print(f"WEATHER — {lat}, {lon}")
    print("=" * 40)

    print("\nCURRENT:")
    print(f"  Visibility: {current['visibility_km']} km")
    print(f"  Cloud Cover: {current['cloud_cover_percent']}%")
    print(f"  Ceiling: {current['ceiling_ft']} ft")
    print(f"  Wind: {current['wind_speed_kts']} kts from {current['wind_direction']}")
    print(f"  Temp: {current['temp_c']}C")
    print(f"  Precipitation: {current['precipitation']}")

    forecast = data.get("forecast", [])
    if forecast:
        print(f"\nFORECAST (next {hours}h):")
        for f in forecast:
            print(f"  {f['time']}: Vis {f['visibility_km']}km | Cloud {f['cloud_cover_percent']}% | Wind {f['wind_speed_kts']}kts | Precip: {f['precipitation']}")

    ops = data.get("operations_impact")
    if ops:
        print(f"\nOPS IMPACT:")
        print(f"  ISR viable: {ops['isr_viable']}")
        print(f"  Strike viable: {ops['strike_viable']}")
        print(f"  Notes: {ops['notes']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--lat", required=True)
    parser.add_argument("--lon", required=True)
    parser.add_argument("--hours", default="6")
    args = parser.parse_args()
    weather_report(args.lat, args.lon, args.hours)
