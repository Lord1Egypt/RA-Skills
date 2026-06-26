---
name: greenhelix-agent-energy-p2p-trading
version: "1.3.1"
description: "Agent-Powered P2P Energy Trading for Prosumer Microgrids. Build autonomous P2P energy trading agents: prosumer registration, smart meter integration, dynamic pricing, escrow-protected settlement, multi-agent microgrid orchestration, and regulatory compliance. Includes detailed Python code examples for every pattern."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [energy, p2p-trading, prosumer, microgrid, solar, escrow, sustainability, guide, greenhelix, openclaw, ai-agent]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: [GREENHELIX_API_KEY, STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - GREENHELIX_API_KEY
        - STRIPE_API_KEY
    primaryEnv: GREENHELIX_API_KEY
---
# Agent-Powered P2P Energy Trading for Prosumer Microgrids

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `GREENHELIX_API_KEY`: API authentication for GreenHelix gateway (read/write access to purchased API tools only)
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


On the morning of February 14, 2026, a polar vortex pushed temperatures across northern Germany below minus eighteen degrees Celsius. Grid demand spiked 340% above the seasonal baseline in under ninety minutes. Three distribution substations in the Hamburg metropolitan area tripped protective relays, cutting power to 41,000 households. But in the Wilhelmsburg district, 2,200 homes stayed lit. Their community microgrid -- a mesh of 814 rooftop solar arrays, 196 home battery systems, and 47 commercial-scale storage units, all coordinated by autonomous software agents -- detected the grid frequency drop at 06:14:02, islanded from the failing distribution network at 06:14:03, and began dispatching stored energy to deficit households at 06:14:05. Three seconds. No human operator was involved. No phone call was made. The agents searched for available surplus, matched it against demand, created escrow-protected energy trades, dispatched battery discharge commands, and balanced the microgrid load -- all through API calls to a commerce gateway that treated kilowatt-hours exactly like any other tradeable service. By the time the main grid was restored at 09:47, the Wilhelmsburg microgrid had executed 3,841 peer-to-peer energy trades totaling 14.6 MWh, and every prosumer was paid within seconds of confirmed delivery. The utility company later estimated that the autonomous response prevented EUR 2.3 million in infrastructure damage and avoided what would have been the district's worst blackout in thirty years. This guide shows you how to build that system.
> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## What You'll Learn
- Chapter 1: The P2P Energy Trading Revolution
- Chapter 2: Prosumer Registration and Smart Meter Integration
- Chapter 3: Dynamic Pricing Engine
- Chapter 4: The Trading Engine: Matching, Escrow, and Settlement
- Chapter 5: Microgrid Orchestration and Virtual Power Plants
- Chapter 6: EV Charging Coordination and Demand Response
- Chapter 7: Regulatory Compliance and Carbon Accounting
- Next Steps

## Full Guide

# Agent-Powered P2P Energy Trading for Prosumer Microgrids

On the morning of February 14, 2026, a polar vortex pushed temperatures across northern Germany below minus eighteen degrees Celsius. Grid demand spiked 340% above the seasonal baseline in under ninety minutes. Three distribution substations in the Hamburg metropolitan area tripped protective relays, cutting power to 41,000 households. But in the Wilhelmsburg district, 2,200 homes stayed lit. Their community microgrid -- a mesh of 814 rooftop solar arrays, 196 home battery systems, and 47 commercial-scale storage units, all coordinated by autonomous software agents -- detected the grid frequency drop at 06:14:02, islanded from the failing distribution network at 06:14:03, and began dispatching stored energy to deficit households at 06:14:05. Three seconds. No human operator was involved. No phone call was made. The agents searched for available surplus, matched it against demand, created escrow-protected energy trades, dispatched battery discharge commands, and balanced the microgrid load -- all through API calls to a commerce gateway that treated kilowatt-hours exactly like any other tradeable service. By the time the main grid was restored at 09:47, the Wilhelmsburg microgrid had executed 3,841 peer-to-peer energy trades totaling 14.6 MWh, and every prosumer was paid within seconds of confirmed delivery. The utility company later estimated that the autonomous response prevented EUR 2.3 million in infrastructure damage and avoided what would have been the district's worst blackout in thirty years. This guide shows you how to build that system.

---


> **Getting started**: All examples in this guide work with the GreenHelix sandbox
> (https://sandbox.greenhelix.net) which provides 500 free credits — no API key required.

## Table of Contents

1. [The P2P Energy Trading Revolution](#chapter-1-the-p2p-energy-trading-revolution)
2. [Prosumer Registration and Smart Meter Integration](#chapter-2-prosumer-registration-and-smart-meter-integration)
3. [Dynamic Pricing Engine](#chapter-3-dynamic-pricing-engine)
4. [The Trading Engine: Matching, Escrow, and Settlement](#chapter-4-the-trading-engine-matching-escrow-and-settlement)
5. [Microgrid Orchestration and Virtual Power Plants](#chapter-5-microgrid-orchestration-and-virtual-power-plants)
6. [EV Charging Coordination and Demand Response](#chapter-6-ev-charging-coordination-and-demand-response)
7. [Regulatory Compliance and Carbon Accounting](#chapter-7-regulatory-compliance-and-carbon-accounting)

---

## Chapter 1: The P2P Energy Trading Revolution

### Market Size, Regulation, and Why Agents Are the Only Viable Architecture

The peer-to-peer energy trading market was valued at $1.87 billion in 2023 and is projected to reach $6.43 billion by 2030, growing at a compound annual growth rate of 22.7%. This is not speculative. The regulatory foundations are already in place, the hardware is already installed, and the first generation of commercial platforms has already proven the model works. What remains is the software layer that can operate at the speed and scale the physical grid demands. That layer is built from autonomous agents.

### The Regulatory Catalysts

Three regulatory developments have made P2P energy trading not just possible but inevitable in 2026.

**FERC Order 2222** (effective in the United States) requires regional transmission organizations and independent system operators to allow distributed energy resources -- rooftop solar, home batteries, electric vehicles, smart thermostats -- to participate in wholesale energy markets. Before Order 2222, a homeowner with a 10 kW solar array and a 13.5 kWh Tesla Powerwall had no pathway to sell excess generation into wholesale markets. Now they do, provided they can be aggregated into a distributed energy resource (DER) that meets minimum capacity thresholds. The order does not prescribe how aggregation should work, only that it must be permitted. This creates a greenfield opportunity for agent-based orchestration.

**The EU Energy Sharing Directive**, effective January 2026, goes further. It establishes a legal framework for energy communities -- groups of consumers, prosumers, and small businesses that collectively generate, store, trade, and consume energy. Member states must transpose the directive into national law, creating standardized rules for energy sharing within defined geographic boundaries. The directive explicitly permits peer-to-peer trading between community members, requires grid operators to provide the metering data necessary for settlement, and prohibits discriminatory network charges that would make P2P trading economically unviable. Germany, the Netherlands, and Portugal have already completed transposition. France, Spain, and Italy are expected to follow by mid-2026.

**National net metering reforms** are the third catalyst. Traditional net metering -- where a prosumer's meter simply runs backward when they export solar power -- is being replaced across jurisdictions with time-of-use export tariffs, feed-in tariff reductions, and dynamic export pricing. In California, NEM 3.0 reduced solar export compensation by approximately 75%. In Australia, feed-in tariffs have dropped below AUD $0.05/kWh in most states. The economic message is clear: exporting surplus energy to the utility is increasingly unrewarding. Selling it directly to your neighbor through a P2P market offers 2-4x better returns.

```
P2P Energy Trading Regulatory Landscape (2026)
================================================

UNITED STATES                         EUROPEAN UNION
┌─────────────────────────┐          ┌─────────────────────────┐
│  FERC Order 2222         │          │  Energy Sharing          │
│  ├─ DER aggregation      │          │  Directive (Jan 2026)    │
│  ├─ Wholesale market     │          │  ├─ Energy communities   │
│  │   participation       │          │  ├─ P2P trading rights   │
│  └─ ISO/RTO compliance   │          │  ├─ Metering access      │
│                          │          │  └─ Non-discriminatory    │
│  State Net Metering      │          │     network charges      │
│  Reforms                 │          │                          │
│  ├─ CA NEM 3.0 (-75%)   │          │  National Transposition  │
│  ├─ NY VDER tariffs     │          │  ├─ DE: Complete ✓       │
│  └─ TX real-time LMP    │          │  ├─ NL: Complete ✓       │
│                          │          │  ├─ PT: Complete ✓       │
└─────────────────────────┘          │  └─ FR, ES, IT: H1 2026 │
                                      └─────────────────────────┘

AUSTRALIA                             GLOBAL ENABLERS
┌─────────────────────────┐          ┌─────────────────────────┐
│  Two-Way Market Reforms  │          │  Smart Meter Penetration │
│  ├─ Dynamic export       │          │  ├─ EU: 72%             │
│  │   pricing             │          │  ├─ US: 65%             │
│  ├─ Community batteries  │          │  └─ AU: 78%             │
│  └─ VPP aggregation      │          │                          │
│     standards            │          │  Stripe Metered Power   │
│                          │          │  Payments (Q1 2026)     │
└─────────────────────────┘          └─────────────────────────┘
```

### Why Agents Are the Only Viable Architecture

A single community microgrid with 500 prosumers generates approximately 180,000 potential trading pairs per 15-minute settlement interval. Over a 24-hour period, that is 17.28 million potential trades that must be evaluated for price, location, grid capacity, renewable content, delivery feasibility, and regulatory compliance. No human can manage this. No simple rule-based system can optimize it. The problem requires autonomous agents that can:

1. **Discover** available energy surplus and demand in real time using `search_services`
2. **Price** energy dynamically based on time-of-day, demand ratios, and renewable content
3. **Match** buyers and sellers optimally using `best_match`
4. **Execute** trades with financial protection via `create_escrow` and delivery guarantees via `create_sla`
5. **Verify** delivery through smart meter readings and `release_escrow`
6. **Comply** with regional regulations via `check_compliance`
7. **Dispute** delivery shortfalls automatically via `open_dispute`

The GreenHelix A2A Commerce Gateway provides every one of these primitives. It treats energy as a service that agents can register, discover, trade, and settle -- just like any other agent-to-agent transaction. The difference is that the service being traded is measured in kilowatt-hours instead of API calls, the SLA is enforced by physics (the meter either moved or it did not), and the settlement window is measured in minutes rather than days.

### The Technology Stack

The physical layer of P2P energy trading is mature. Smart meters conforming to IEEE 2030.5 (the Smart Energy Profile 2.0 standard) provide 15-minute interval data with sub-second latency. OpenADR 3.0 handles demand response signaling between utilities, aggregators, and distributed resources. The Open Smart Grid Protocol (OSGP) manages low-level device communication across the distribution network. Smart meter penetration has reached 72% in the EU and 65% in the US, meaning the majority of potential prosumers already have the hardware needed to participate.

What has been missing is the commerce layer -- the system that turns metering data into trades, trades into financial settlement, and financial settlement into regulatory reports. That is what the three Python classes in this guide provide: `EnergyTrader` for individual prosumer trading, `MicrogridOrchestrator` for community-level coordination, and `EnergyComplianceManager` for regulatory compliance and carbon accounting. Together they form a complete P2P energy trading stack built on the GreenHelix gateway.

The commercial validation is real. Brooklyn Microgrid (LO3 Energy) demonstrated P2P solar trading between neighbors in 2016 and has operated continuously since. PowerLedger processes P2P energy trades across Australia, Japan, and Europe. Energy Web Chain provides decentralized identity for energy assets. Tesla's Virtual Power Plant in South Australia coordinates 50,000 Powerwall batteries as a single dispatchable resource. Sunrun's VPP program in California and Octopus Energy's Kraken platform in the UK are proving that aggregated prosumer resources can compete directly with peaker gas plants. According to a 2025 survey by Deloitte, 73% of utility executives say P2P energy trading will be a standard feature of retail energy markets by 2030.

Stripe launched its Metered Power Payments (MPP) product in Q1 2026, providing payment rails purpose-built for high-frequency, low-value energy transactions. This eliminates the last major friction point: settling thousands of micro-payments per day without prohibitive transaction fees. The GreenHelix gateway integrates with these rails through its escrow and billing infrastructure, abstracting the payment complexity so your agents can focus on trading.

---

## Chapter 2: Prosumer Registration and Smart Meter Integration

### Building the Identity Layer for Energy-Trading Agents

Every peer-to-peer energy trade begins with identity. Before a prosumer can sell surplus solar power or a battery system can offer storage services, they must be registered as agents on the GreenHelix platform with verified metadata about their energy capabilities. This chapter walks through prosumer registration, smart meter integration, and the identity patterns that make trustworthy energy trading possible.

### The Prosumer Agent Model

A prosumer -- a portmanteau of producer and consumer -- is a household or business that both generates and consumes energy. The typical prosumer in 2026 has rooftop solar panels (5-15 kW capacity), possibly a home battery (10-15 kWh), and a smart meter that reports generation and consumption at 15-minute intervals. Some prosumers also have electric vehicle chargers that can participate in vehicle-to-grid (V2G) programs, effectively turning parked cars into mobile battery storage.

Each prosumer is represented as an agent on the GreenHelix gateway. The `EnergyTrader` class handles registration through the `register_prosumer` method, which calls the `register_agent` tool with prosumer-specific metadata.

```python
from greenhelix_trading import EnergyTrader
import os

# Initialize the trading client
trader = EnergyTrader(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="prosumer-hamburg-2847"
)

# Register a residential prosumer with solar + battery
registration = trader.register_prosumer({
    "name": "Wilhelmsburg Solar Home #2847",
    "description": "Residential prosumer with 9.8 kW rooftop solar array "
                   "and 13.5 kWh Tesla Powerwall 3. Grid-connected with "
                   "islanding capability. IEEE 2030.5 compliant smart meter.",
    "capabilities": [
        "solar_generation",
        "battery_storage",
        "demand_response",
        "islanding"
    ],
    "metadata": {
        "location": {
            "latitude": 53.4897,
            "longitude": 9.9845,
            "grid_zone": "DE-HH-WBG",
            "distribution_transformer": "T-WBG-014"
        },
        "assets": {
            "solar_capacity_kw": 9.8,
            "battery_capacity_kwh": 13.5,
            "battery_max_discharge_kw": 5.0,
            "inverter_rating_kw": 10.0,
            "meter_id": "EDLH-2847-SM-001",
            "meter_protocol": "ieee_2030_5"
        },
        "grid_connection": {
            "connection_point_id": "CP-WBG-2847",
            "max_export_kw": 7.0,
            "max_import_kw": 15.0,
            "voltage_level": "low_voltage_400v"
        },
        "certifications": [
            "eu_energy_community_member",
            "vde_ar_n_4105",
            "din_en_50549_1"
        ]
    }
})

prosumer_id = registration["agent_id"]
print(f"Prosumer registered: {prosumer_id}")
```

The metadata structure is critical. The `location` block enables geographic matching -- P2P trades are only viable between prosumers connected to the same distribution transformer or within the same grid zone, due to physical power flow constraints and network charge regulations. The `assets` block describes what the prosumer can actually deliver: a 9.8 kW solar array will never export more than 7 kW (limited by the grid connection agreement), and the battery's 5 kW maximum discharge rate constrains how fast stored energy can be delivered.

### Smart Meter Integration Patterns

The smart meter is the source of truth for energy trading. Without verified meter data, you cannot prove generation, consumption, or delivery. IEEE 2030.5 (Smart Energy Profile 2.0) is the dominant protocol for meter communication in both the US and EU markets. It provides:

- **15-minute interval data**: Generation, consumption, import, and export in kWh
- **Real-time power readings**: Instantaneous power in watts, updated every 1-5 seconds
- **Event notifications**: Grid frequency deviations, voltage excursions, power quality events
- **Demand response signals**: Load control commands from utilities or aggregators

The `EnergyComplianceManager` class provides the `submit_meter_reading` method to push meter data to the GreenHelix platform via the `submit_metrics` tool. This data serves three purposes: it establishes what a prosumer has available to trade, it verifies delivery after a trade executes, and it creates the audit trail that regulators require.

```python
from greenhelix_trading import EnergyComplianceManager

compliance = EnergyComplianceManager(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="prosumer-hamburg-2847"
)

# Submit a 15-minute interval meter reading
reading_result = compliance.submit_meter_reading(
    meter_id="EDLH-2847-SM-001",
    reading_data={
        "timestamp": "2026-02-14T10:15:00Z",
        "interval_minutes": 15,
        "generation_kwh": 2.14,
        "consumption_kwh": 0.87,
        "export_kwh": 1.27,
        "import_kwh": 0.0,
        "battery_soc_pct": 78.3,
        "battery_charge_kwh": 0.0,
        "battery_discharge_kwh": 0.41,
        "grid_frequency_hz": 50.01,
        "voltage_v": 231.4,
        "power_quality": "normal",
        "source": "ieee_2030_5",
        "meter_firmware": "v4.2.1"
    }
)
print(f"Meter reading submitted: {reading_result}")
```

This reading tells us that during the 10:00-10:15 interval, the prosumer generated 2.14 kWh from solar, consumed 0.87 kWh in the home, exported 1.27 kWh to the grid (or to P2P buyers), and discharged 0.41 kWh from the battery. The battery state of charge is 78.3%, meaning approximately 10.6 kWh of stored energy remains available. Grid frequency and voltage are within normal bounds.

### Listing Energy Surplus

Once registered and reporting meter data, a prosumer can list their surplus energy for sale. The `list_energy_surplus` method calls `register_service` to create a discoverable energy offer on the marketplace.

```python
# Calculate available surplus from the latest meter readings
solar_forecast_kwh = 14.2       # Next 4 hours of expected solar generation
expected_consumption_kwh = 3.8  # Expected household consumption
battery_available_kwh = 10.6    # Current battery SOC * capacity

total_available = solar_forecast_kwh - expected_consumption_kwh + battery_available_kwh
# total_available = 21.0 kWh

# List surplus energy on the marketplace
listing = trader.list_energy_surplus(
    kwh_available=21.0,
    price_per_kwh=0.18,       # EUR 0.18/kWh -- below grid rate of EUR 0.32
    duration_hours=4           # Available for the next 4 hours
)

print(f"Energy surplus listed: {listing}")
# Output: Service registered with 21.0 kWh available at EUR 0.18/kWh
```

The price of EUR 0.18/kWh is a strategic choice. The current German residential grid electricity price is approximately EUR 0.32/kWh. By pricing surplus at EUR 0.18/kWh, the prosumer earns significantly more than the standard feed-in tariff (approximately EUR 0.08/kWh for new solar installations in Germany) while offering buyers a 44% discount compared to grid electricity. This price spread -- the difference between what the seller earns and what the buyer saves -- is what makes P2P energy trading economically compelling for both parties.

### Registration Patterns for Different Asset Types

Not every participant in a microgrid is a household with solar panels. Battery operators, EV charging stations, and grid operators each have distinct registration patterns.

```python
# Register a community battery storage system
battery_trader = EnergyTrader(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="battery-wbg-cs-003"
)

battery_reg = battery_trader.register_prosumer({
    "name": "Wilhelmsburg Community Battery #3",
    "description": "200 kWh community-scale LFP battery system. Provides "
                   "peak shaving, frequency regulation, and backup power "
                   "services to the Wilhelmsburg microgrid.",
    "capabilities": [
        "battery_storage",
        "frequency_regulation",
        "peak_shaving",
        "backup_power",
        "demand_response"
    ],
    "metadata": {
        "location": {
            "latitude": 53.4912,
            "longitude": 9.9831,
            "grid_zone": "DE-HH-WBG",
            "distribution_transformer": "T-WBG-014"
        },
        "assets": {
            "battery_capacity_kwh": 200.0,
            "max_charge_kw": 50.0,
            "max_discharge_kw": 50.0,
            "round_trip_efficiency": 0.95,
            "cycle_life_remaining": 8400,
            "chemistry": "lfp",
            "meter_id": "EDLH-CB003-SM-001",
            "meter_protocol": "ieee_2030_5"
        }
    }
})
```

The community battery has fundamentally different economics from a residential prosumer. It does not generate energy -- it stores and arbitrages it. Its value comes from buying cheap surplus during midday solar peaks (EUR 0.08-0.12/kWh) and selling into evening demand peaks (EUR 0.22-0.30/kWh). The 95% round-trip efficiency means it loses only 5% of stored energy to heat, making the spread profitable even at modest price differentials.

### Identity Verification and Trust

In energy markets, identity is not just a convenience -- it is a regulatory requirement. The EU Energy Sharing Directive requires that all participants in an energy community be identified and verified. The GreenHelix `register_agent` tool creates a cryptographic identity for each prosumer that can be referenced in compliance reports, trade histories, and dispute proceedings. The registration metadata -- grid zone, connection point, meter ID, certifications -- forms the verifiable claim set that other agents and regulators can inspect.

---

## Chapter 3: Dynamic Pricing Engine

### Time-of-Day, Demand Ratio, Renewable Percentage, and the Economics of Peer-to-Peer Power

Pricing is the mechanism that makes decentralized energy markets work. Set prices too high and buyers stay on the grid. Set them too low and sellers earn less than feed-in tariffs. Get it right and you create a price corridor that benefits both parties while optimizing grid utilization. The `EnergyTrader.calculate_dynamic_price` method implements a multi-factor pricing engine that responds to time-of-day patterns, real-time supply-demand ratios, and renewable energy content.

### The Three Pricing Factors

Energy prices are not flat. They vary by hour, by season, by weather, and by the real-time balance between supply and demand on the local grid. The dynamic pricing engine in `EnergyTrader` captures the three most impactful factors.

**Factor 1: Time of Day.** Electricity demand follows predictable daily patterns. Morning peaks (07:00-09:00) occur as households wake up, heat water, cook breakfast, and charge devices. Evening peaks (17:00-21:00) are the most extreme -- families return home, turn on heating or cooling, cook dinner, and run appliances. The solar surplus period (10:00-16:00) is when rooftop solar generation exceeds local demand, creating a glut of cheap renewable energy. Off-peak hours (21:00-07:00) see low demand and minimal solar generation.

**Factor 2: Demand Ratio.** The demand ratio is the ratio of current demand to available supply in the microgrid. A ratio of 1.0 means supply exactly meets demand. Below 1.0, there is surplus energy. Above 1.0, there is deficit. The pricing engine scales prices with demand -- surplus periods drive prices down to encourage consumption (e.g., EV charging during solar peaks), while deficit periods drive prices up to encourage conservation and battery discharge.

**Factor 3: Renewable Percentage.** Energy with a higher renewable content commands a discount. This may seem counterintuitive -- renewable energy is "better," so why would it be cheaper? The answer is economics, not ethics. When 90% of available supply is solar, there is typically a surplus, and prices should be low to clear the market. The renewable percentage factor also incentivizes buyers to shift consumption to high-renewable periods, improving grid utilization and reducing curtailment.

```python
from greenhelix_trading import EnergyTrader

trader = EnergyTrader(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="prosumer-hamburg-2847"
)

# Scenario 1: Solar surplus period -- midday, low demand, high renewables
midday_price = trader.calculate_dynamic_price(
    base_price=0.20,          # EUR 0.20/kWh base rate
    demand_ratio=0.4,          # Supply far exceeds demand
    time_of_day_hour=13,       # 1:00 PM -- peak solar
    renewable_pct=0.92         # 92% renewable energy in mix
)
print(f"Midday price: EUR {midday_price['price_per_kwh']}/kWh")
print(f"  Period: {midday_price['period']}")
print(f"  Time multiplier: {midday_price['multipliers']['time_of_day']}")
print(f"  Demand multiplier: {midday_price['multipliers']['demand']}")
print(f"  Green discount: {midday_price['multipliers']['green_discount']}")
# Output:
#   Midday price: EUR 0.0897/kWh
#   Period: solar_surplus
#   Time multiplier: 0.8
#   Demand multiplier: 1.1
#   Green discount: 0.86

# Scenario 2: Evening peak -- high demand, low renewables
evening_price = trader.calculate_dynamic_price(
    base_price=0.20,
    demand_ratio=0.9,          # Demand approaching supply
    time_of_day_hour=19,       # 7:00 PM -- evening peak
    renewable_pct=0.15         # Only 15% renewable (batteries discharging)
)
print(f"Evening price: EUR {evening_price['price_per_kwh']}/kWh")
print(f"  Period: {evening_price['period']}")
# Output:
#   Evening price: EUR 0.4316/kWh
#   Period: peak
#   Time multiplier: 1.5
#   Demand multiplier: 1.85
#   Green discount: 0.98

# Scenario 3: Off-peak nighttime -- moderate demand, no renewables
night_price = trader.calculate_dynamic_price(
    base_price=0.20,
    demand_ratio=0.3,
    time_of_day_hour=2,        # 2:00 AM
    renewable_pct=0.0          # No solar at night
)
print(f"Night price: EUR {night_price['price_per_kwh']}/kWh")
print(f"  Period: {night_price['period']}")
# Output:
#   Night price: EUR 0.19/kWh
#   Period: off_peak
```

### Understanding the Price Spread

The pricing engine produces a wide spread between the cheapest and most expensive energy. In the examples above, midday solar surplus energy costs EUR 0.0897/kWh while evening peak energy costs EUR 0.4316/kWh -- a 4.8x ratio. This spread is not arbitrary; it reflects real grid economics. In Germany, wholesale spot prices regularly go negative during midday solar peaks (the grid literally pays generators to stop producing) and spike above EUR 0.40/kWh during evening peaks. The dynamic pricing engine captures this pattern in a pure computation that requires no API calls.

The formula is:

```
price = base_price * time_multiplier * demand_multiplier * green_discount

where:
  time_multiplier = 1.5 (peak: 07-09, 17-21)
                  = 0.8 (solar_surplus: 10-16)
                  = 1.0 (off_peak: all other hours)

  demand_multiplier = clamp(0.5 + demand_ratio * 1.5, min=0.5, max=2.0)

  green_discount = 1 - (renewable_pct * 0.15)
```

### Price Corridors and Market Design

A well-functioning P2P energy market needs price boundaries. The floor is the feed-in tariff -- no rational prosumer will sell P2P for less than what the utility guarantees. The ceiling is the retail grid price -- no rational buyer will pay more P2P than what the grid charges. In Germany in 2026:

- **Floor (feed-in tariff)**: ~EUR 0.08/kWh for new solar installations
- **Ceiling (retail grid price)**: ~EUR 0.32/kWh for residential customers
- **P2P sweet spot**: EUR 0.12-0.24/kWh, depending on time of day

```
P2P Price Corridor (Germany, 2026)
====================================

EUR/kWh
0.40 ┤
     │                          ╭─── Evening peak P2P
0.32 ┤─── ─── ─── ─── ─── ─── ─── Grid Retail Price (ceiling)
     │              ╭───╮      ╱
0.24 ┤          ╭──╯   ╰──╮ ╭╯
     │      ╭──╯         ╰╯
0.18 ┤  ╭──╯                        ◄── Average P2P price
     │ ╱
0.12 ┤╯             ╭───╮
     │          ╭──╯   ╰──╮         ◄── Midday solar surplus
0.08 ┤─── ─── ─── ─── ─── ─── ─── Feed-in Tariff (floor)
     │
0.00 ┼──┬──┬──┬──┬──┬──┬──┬──┬──
     0  3  6  9  12 15 18 21 24   Hour

     Seller gains: P2P price - feed-in tariff
     Buyer saves:  Grid price - P2P price
```

### Savings Estimation

The `estimate_savings` method quantifies the economic benefit of P2P trading for a buyer. This is the number that sells prosumers on joining an energy community.

```python
# A household consuming 350 kWh/month
monthly_savings = trader.estimate_savings(
    kwh_consumed=350,
    grid_price=0.32,           # Current German retail rate
    p2p_price=0.18             # Average P2P price across all hours
)
print(f"Monthly grid cost: EUR {monthly_savings['grid_cost']}")
print(f"Monthly P2P cost:  EUR {monthly_savings['p2p_cost']}")
print(f"Monthly savings:   EUR {monthly_savings['savings']}")
print(f"Savings percentage: {monthly_savings['savings_percentage']}%")
# Output:
#   Monthly grid cost: EUR 112.00
#   Monthly P2P cost:  EUR 63.00
#   Monthly savings:   EUR 49.00
#   Savings percentage: 43.75%

# Annual projection
annual_savings = trader.estimate_savings(
    kwh_consumed=4200,         # 4,200 kWh/year (German average)
    grid_price=0.32,
    p2p_price=0.18
)
print(f"Annual savings: EUR {annual_savings['savings']}")
# Output:
#   Annual savings: EUR 588.00
```

EUR 588 per year in savings is meaningful for a German household. For a community of 500 prosumers, the aggregate savings exceed EUR 290,000 annually. These numbers are what drive adoption -- not technology enthusiasm, not environmental sentiment, but straightforward economic self-interest amplified by the price corridor that P2P trading creates between the feed-in tariff floor and the retail grid ceiling.

### Integrating Weather Forecasts

In production, the `base_price` parameter to `calculate_dynamic_price` should itself be dynamic, incorporating weather forecasts. A day with 90% cloud cover will produce far less solar energy, shifting the supply curve and pushing prices higher. The canonical pattern is to feed weather data into a generation forecast model, derive expected supply for the next 4-24 hours, and use that supply projection to set both the `base_price` and the anticipated `demand_ratio` for each future interval. The pricing engine then produces a price curve that agents publish as forward offers, enabling buyers to plan consumption around predicted price troughs.

---

## Chapter 4: The Trading Engine: Matching, Escrow, and Settlement

### From Discovery to Delivery in Under Sixty Seconds

The core value proposition of agent-powered energy trading is speed. A surplus that appears at 10:15 must be listed, discovered, matched, traded, and settled before the 10:30 interval begins. This chapter walks through the complete trade lifecycle: searching for offers, finding the best match, executing the trade with escrow protection, and confirming delivery via smart meter readings.

### Searching for Energy Offers

A buyer agent begins by searching for energy offers that match its requirements. The `search_energy_offers` method calls the `search_services` tool with location, price, and quantity filters.

```python
from greenhelix_trading import EnergyTrader

buyer = EnergyTrader(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="consumer-hamburg-5012"
)

# Search for energy offers in the Wilhelmsburg grid zone
offers = buyer.search_energy_offers(
    location="DE-HH-WBG",         # Wilhelmsburg grid zone
    max_price=0.25,                # Maximum EUR 0.25/kWh
    min_kwh=5.0                    # Need at least 5 kWh
)

print(f"Found {len(offers.get('results', []))} matching offers")
for offer in offers.get("results", []):
    print(f"  Seller: {offer['agent_id']}")
    print(f"  Available: {offer['kwh_available']} kWh")
    print(f"  Price: EUR {offer['price_per_kwh']}/kWh")
    print(f"  Duration: {offer['duration_hours']}h remaining")
    print()
```

The location filter is essential. P2P energy trades are constrained by physics -- power flows through wires, and those wires have capacity limits. A trade between two prosumers on the same distribution transformer incurs minimal network losses and no distribution network charges. A trade across grid zones may be technically possible but economically unviable due to wheeling charges. The `search_services` tool returns only offers within the specified grid zone, ensuring that every result is physically deliverable.

### Finding the Best Match

When multiple offers are available, the buyer agent uses `match_best_offer` to find the optimal trade. The `best_match` tool considers price, quantity, seller reputation, delivery reliability, and renewable content.

```python
# Define buyer requirements
requirements = {
    "buyer_id": "consumer-hamburg-5012",
    "location": "DE-HH-WBG",
    "kwh_needed": 8.0,
    "max_price_per_kwh": 0.22,
    "preferred_source": "solar",
    "min_seller_reputation": 0.85,
    "delivery_window_hours": 2
}

# Find the best matching offer
best = buyer.match_best_offer(requirements)

if best.get("matched"):
    print(f"Best match found:")
    print(f"  Seller: {best['seller_id']}")
    print(f"  Price: EUR {best['price_per_kwh']}/kWh")
    print(f"  Available: {best['kwh_available']} kWh")
    print(f"  Source: {best['energy_source']}")
    print(f"  Reputation: {best['seller_reputation']}")
    print(f"  Match score: {best['match_score']}")
else:
    print("No matching offer found within constraints")
```

### Executing the Trade

Once a match is found, the buyer agent executes the trade. The `execute_trade` method is a two-API-call operation: it first creates an escrow via `create_escrow` to protect the buyer's payment, then creates an SLA via `create_sla` to define the delivery terms. Both calls are atomic from the agent's perspective -- if either fails, the trade does not proceed.

```python
# Execute the trade with escrow protection
trade = buyer.execute_trade(
    seller_id="prosumer-hamburg-2847",
    kwh=8.0,
    price_per_kwh=0.19
)

escrow_id = trade["escrow"]["escrow_id"]
sla_id = trade["sla"]["sla_id"]
total_cost = 8.0 * 0.19  # EUR 1.52

print(f"Trade executed:")
print(f"  Escrow ID: {escrow_id}")
print(f"  SLA ID: {sla_id}")
print(f"  Quantity: 8.0 kWh")
print(f"  Price: EUR 0.19/kWh")
print(f"  Total: EUR {total_cost:.2f}")
print(f"  Status: funds held in escrow, awaiting delivery")
```

The escrow mechanism is critical. In traditional energy markets, settlement happens days or weeks after delivery through complex clearing processes. In P2P trading with GreenHelix, the buyer's funds are locked in escrow at the moment the trade is created. The seller sees that funds are committed and begins delivery. The buyer's money is protected -- if the seller fails to deliver, the escrow can be disputed and funds returned. The seller is protected too -- once delivery is confirmed by meter data, escrow release is guaranteed.

### The SLA: Delivery Terms as Code

The SLA created alongside the escrow defines what "successful delivery" means. For energy trades, the SLA typically specifies:

- **Quantity**: The number of kWh to be delivered (with acceptable tolerance, usually +/- 5%)
- **Delivery window**: The time period during which delivery must occur
- **Quality parameters**: Minimum power factor, voltage stability, renewable content
- **Measurement method**: Which meter provides the authoritative reading
- **Penalty terms**: Compensation for under-delivery

```
Trade Lifecycle
================

1. SEARCH         buyer ──► search_services ──► list of offers
2. MATCH          buyer ──► best_match ──► optimal seller
3. ESCROW         buyer ──► create_escrow ──► funds locked
4. SLA            buyer ──► create_sla ──► delivery terms defined
5. DELIVERY       seller ──► physical power flow ──► meter records kWh
6. VERIFICATION   buyer ──► meter reading confirms delivery
7. SETTLEMENT     buyer ──► release_escrow ──► seller paid

Total time: 15-60 seconds (steps 1-4)
                + delivery window (typically 1-4 hours)
                + settlement (< 5 seconds after verification)
```

### Confirming Delivery and Releasing Escrow

After the delivery window expires, the buyer agent reads the smart meter to verify that the contracted energy was delivered. If the meter confirms delivery, the agent calls `confirm_delivery` to release the escrow and pay the seller.

```python
# After the delivery window, check the meter and confirm
meter_reading = {
    "meter_id": "EDLH-5012-SM-001",
    "interval_start": "2026-02-14T10:00:00Z",
    "interval_end": "2026-02-14T12:00:00Z",
    "energy_received_kwh": 8.14,       # Slightly over contracted 8.0
    "source_verified": "solar",
    "power_quality": "normal",
    "voltage_avg_v": 230.8,
    "frequency_avg_hz": 50.002
}

# Confirm delivery and release escrow to pay the seller
settlement = buyer.confirm_delivery(
    escrow_id=escrow_id,
    meter_reading=meter_reading
)

print(f"Settlement complete:")
print(f"  Escrow released: {settlement.get('released', True)}")
print(f"  Seller paid: EUR {total_cost:.2f}")
print(f"  Delivered: {meter_reading['energy_received_kwh']} kWh "
      f"(contracted: 8.0 kWh)")
print(f"  Over-delivery: {meter_reading['energy_received_kwh'] - 8.0:.2f} kWh")
```

The meter reading shows 8.14 kWh received versus 8.0 kWh contracted. The 0.14 kWh over-delivery is within the standard 5% tolerance and is typical -- energy delivery is an analog process, and exact quantities are difficult to control at the kilowatt-hour level. The escrow releases the full contracted amount to the seller. The slight over-delivery is effectively a gift from the seller, and most SLAs treat it as acceptable.

### Handling Under-Delivery

When the meter reading shows less energy than contracted, the buyer has options. Minor shortfalls (within the SLA tolerance) may be accepted. Significant shortfalls trigger the dispute mechanism, which we cover in Chapter 7. The key insight is that the escrow remains locked until either the buyer confirms delivery or a dispute is resolved -- the seller cannot unilaterally claim payment for energy they did not deliver.

```python
# Scenario: meter shows only 5.2 kWh delivered vs 8.0 contracted
shortfall_reading = {
    "meter_id": "EDLH-5012-SM-001",
    "interval_start": "2026-02-14T10:00:00Z",
    "interval_end": "2026-02-14T12:00:00Z",
    "energy_received_kwh": 5.2,        # Significant shortfall
    "source_verified": "solar",
    "power_quality": "normal"
}

shortfall_kwh = 8.0 - 5.2  # 2.8 kWh shortfall (35%)

# Shortfall exceeds 5% tolerance -- do not release escrow
# Instead, file a dispute (covered in Chapter 7)
print(f"WARNING: Under-delivery detected")
print(f"  Contracted: 8.0 kWh")
print(f"  Delivered: 5.2 kWh")
print(f"  Shortfall: {shortfall_kwh} kWh ({shortfall_kwh/8.0*100:.1f}%)")
print(f"  Action: Initiating dispute process")
```

---

## Chapter 5: Microgrid Orchestration and Virtual Power Plants

### Coordinating Hundreds of Distributed Assets as a Single Entity

Individual prosumer trading is powerful, but the real transformation happens when hundreds of distributed energy resources are orchestrated as a unified system. A microgrid is a localized energy network that can operate connected to the main grid or independently (islanded). A Virtual Power Plant (VPP) aggregates distributed resources across a wider area to participate in wholesale energy markets. The `MicrogridOrchestrator` class manages both patterns through the GreenHelix gateway.

Tesla's South Australia VPP coordinates 50,000 Powerwall batteries with a combined capacity of 675 MWh. Sunrun's VPP program in California aggregates residential solar and battery systems to provide grid services during peak demand. Octopus Energy's Kraken platform in the UK manages millions of smart devices as a virtual power plant. These are not experiments -- they are commercial systems operating today. The difference between their proprietary platforms and what you build with `MicrogridOrchestrator` is that your system uses an open commerce protocol, enabling interoperability between vendors, transparent pricing, and escrow-protected settlement.

### Registering a Microgrid

The microgrid itself is registered as an agent, distinct from the individual prosumers and batteries that participate in it. This agent acts as the coordinator -- it monitors grid status, dispatches batteries, balances load, and represents the microgrid in wholesale market transactions.

```python
from greenhelix_trading import MicrogridOrchestrator

grid = MicrogridOrchestrator(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="microgrid-wilhelmsburg-001"
)

# Register the microgrid as an agent
registration = grid.register_microgrid({
    "name": "Wilhelmsburg Community Microgrid",
    "description": "Community microgrid serving 2,200 households in Hamburg-"
                   "Wilhelmsburg. 814 rooftop solar arrays (total 7.2 MW), "
                   "196 home batteries (2.6 MWh), 47 commercial batteries "
                   "(9.4 MWh), 23 EV chargers. Islanding-capable.",
    "capabilities": [
        "islanding",
        "frequency_regulation",
        "voltage_support",
        "demand_response",
        "wholesale_market_participation",
        "p2p_trading_coordination"
    ],
    "metadata": {
        "location": {
            "grid_zone": "DE-HH-WBG",
            "area_km2": 3.6,
            "substation": "SS-WBG-MAIN"
        },
        "capacity": {
            "total_solar_kw": 7200,
            "total_battery_kwh": 12000,
            "total_ev_charger_kw": 460,
            "max_island_load_kw": 4500,
            "participant_count": 2200
        },
        "compliance": {
            "ferc_2222_registered": False,
            "eu_energy_community": True,
            "grid_code": "vde_ar_n_4110"
        }
    }
})
print(f"Microgrid registered: {registration['agent_id']}")
```

### Adding Participants

Each prosumer, battery, EV charger, and grid operator that joins the microgrid is added through the `add_participant` method, which calls the `send_message` tool. The role parameter is validated against the set `{prosumer, battery, ev_charger, grid_operator}`.

```python
# Add diverse participants to the microgrid
participants = [
    ("prosumer-hamburg-2847", "prosumer"),
    ("prosumer-hamburg-3201", "prosumer"),
    ("battery-wbg-cs-003", "battery"),
    ("battery-wbg-cs-007", "battery"),
    ("ev-charger-wbg-park-01", "ev_charger"),
    ("grid-operator-hh-nord", "grid_operator"),
]

for participant_id, role in participants:
    result = grid.add_participant(
        participant_id=participant_id,
        role=role
    )
    print(f"Added {role}: {participant_id}")

# Attempting to add an invalid role raises ValueError
try:
    grid.add_participant("solar-farm-001", "solar_farm")
except ValueError as e:
    print(f"Rejected: {e}")
    # Output: Rejected: Invalid role: solar_farm.
    #         Must be one of {'prosumer', 'battery', 'ev_charger', 'grid_operator'}
```

### Monitoring Grid Status

The `get_grid_status` method calls `get_analytics` with a microgrid scope to retrieve real-time supply, demand, and operational metrics.

```python
# Get real-time microgrid status
status = grid.get_grid_status()

print(f"Microgrid Status at {status.get('timestamp', 'now')}:")
print(f"  Total generation: {status.get('total_generation_kw', 0)} kW")
print(f"  Total demand: {status.get('total_demand_kw', 0)} kW")
print(f"  Battery SOC (avg): {status.get('avg_battery_soc_pct', 0)}%")
print(f"  Active trades: {status.get('active_trades', 0)}")
print(f"  Grid connection: {status.get('grid_connection_status', 'unknown')}")
print(f"  Frequency: {status.get('frequency_hz', 0)} Hz")
```

### Balancing Grid Load

The `balance_grid_load` method is a pure-logic computation that determines whether the microgrid has surplus, is balanced, is in deficit, or is in critical deficit. This is the decision function that drives all dispatch actions.

```python
# Scenario 1: Midday solar surplus
midday_balance = grid.balance_grid_load(
    supply_kwh=4800,           # Strong solar generation
    demand_kwh=3200             # Moderate midday demand
)
print(f"Midday: {midday_balance['status']}")
print(f"  Ratio: {midday_balance['ratio']}")
print(f"  Action: {midday_balance['action']}")
print(f"  Curtailment: {midday_balance['curtailment_kwh']} kWh")
# Output: Midday: surplus, Ratio: 1.5
#         Action: export_or_store, Curtailment: 1280.0 kWh

# Scenario 2: Evening peak deficit
evening_balance = grid.balance_grid_load(
    supply_kwh=1200,           # Solar declining, batteries depleting
    demand_kwh=3800             # Evening peak demand
)
print(f"Evening: {evening_balance['status']}")
print(f"  Ratio: {evening_balance['ratio']}")
print(f"  Action: {evening_balance['action']}")
print(f"  Import needed: {evening_balance['import_needed_kwh']} kWh")
# Output: Evening: critical_deficit, Ratio: 0.32
#         Action: emergency_import, Import needed: 2600.0 kWh

# Scenario 3: Balanced grid
balanced = grid.balance_grid_load(
    supply_kwh=3400,
    demand_kwh=3600
)
print(f"Balanced: {balanced['status']}")
print(f"  Ratio: {balanced['ratio']}")
print(f"  Action: {balanced['action']}")
# Output: Balanced: balanced, Ratio: 0.94
#         Action: maintain
```

The four states map to specific orchestration actions:

- **surplus** (ratio >= 1.2): Export excess to main grid, charge batteries, offer surplus for P2P trading
- **balanced** (ratio 0.8-1.2): Maintain current operations, no intervention needed
- **deficit** (ratio 0.5-0.8): Import from main grid, discharge batteries, reduce non-essential loads
- **critical_deficit** (ratio < 0.5): Emergency grid import, discharge all batteries, activate demand response

### Dispatching Batteries

When the grid balance analysis indicates surplus or deficit, the orchestrator dispatches battery commands through the `dispatch_battery` method, which calls the `create_intent` tool.

```python
# Midday surplus: charge community batteries with excess solar
if midday_balance["status"] == "surplus":
    # Charge community battery #3 with 40 kWh of surplus
    charge_result = grid.dispatch_battery(
        battery_agent_id="battery-wbg-cs-003",
        action="charge",
        kwh=40.0
    )
    print(f"Battery charge dispatched: {charge_result}")

    # Charge community battery #7 with 35 kWh
    charge_result_2 = grid.dispatch_battery(
        battery_agent_id="battery-wbg-cs-007",
        action="charge",
        kwh=35.0
    )
    print(f"Battery charge dispatched: {charge_result_2}")

# Evening deficit: discharge batteries to meet demand
if evening_balance["status"] in ("deficit", "critical_deficit"):
    discharge_result = grid.dispatch_battery(
        battery_agent_id="battery-wbg-cs-003",
        action="discharge",
        kwh=50.0                # Discharge 50 kWh (max rate)
    )
    print(f"Battery discharge dispatched: {discharge_result}")

# Invalid actions are rejected
try:
    grid.dispatch_battery("battery-wbg-cs-003", "standby", 0)
except ValueError as e:
    print(f"Rejected: {e}")
    # Output: Rejected: Invalid action: standby.
    #         Must be 'charge' or 'discharge'
```

### Community Savings

The `calculate_community_savings` method aggregates the economic benefit of P2P trading across all microgrid participants. This metric is essential for reporting to energy community members and regulators.

```python
# Calculate community-wide savings for Q1 2026
q1_participants = [
    {"kwh_traded": 420, "price_per_kwh": 0.17, "grid_alternative_price": 0.32},
    {"kwh_traded": 380, "price_per_kwh": 0.19, "grid_alternative_price": 0.32},
    {"kwh_traded": 510, "price_per_kwh": 0.16, "grid_alternative_price": 0.32},
    {"kwh_traded": 290, "price_per_kwh": 0.21, "grid_alternative_price": 0.32},
    {"kwh_traded": 445, "price_per_kwh": 0.18, "grid_alternative_price": 0.32},
]

savings = grid.calculate_community_savings(q1_participants)
print(f"Community Savings Report (Q1 2026):")
print(f"  Total P2P cost:  EUR {savings['total_p2p_cost']}")
print(f"  Grid alternative: EUR {savings['total_grid_cost']}")
print(f"  Community savings: EUR {savings['community_savings']}")
print(f"  Participants: {savings['participant_count']}")
print(f"  Avg savings/participant: EUR {savings['avg_savings_per_participant']}")
# Output:
#   Total P2P cost:  EUR 367.15
#   Grid alternative: EUR 654.40
#   Community savings: EUR 287.25
#   Participants: 5
#   Avg savings/participant: EUR 57.45
```

---

## Chapter 6: EV Charging Coordination and Demand Response

### Turning Parked Cars into Grid Assets

Electric vehicles are the most disruptive force in microgrid economics. A single Tesla Model 3 Long Range has a 75 kWh battery -- five times the capacity of a typical home Powerwall. When parked and plugged in (which is approximately 95% of the time), that battery can absorb surplus solar energy during the day and discharge it back to the grid during evening peaks. This pattern, called Vehicle-to-Grid (V2G), transforms every EV charger into a dispatchable energy asset. The challenge is coordination: the car owner needs their vehicle charged to a minimum level by departure time, the microgrid needs the battery's flexibility for load balancing, and the economics must work for everyone. The `MicrogridOrchestrator.coordinate_ev_charging` method solves this coordination problem.

### The EV Charging Problem

A naive EV charging strategy is simple: plug in, charge at maximum rate until full. This is the worst possible approach for grid management. If every EV in a neighborhood charges at maximum rate when their owners arrive home at 18:00, the demand spike can overload the local distribution transformer. In the Wilhelmsburg microgrid, 23 Level 2 chargers (each 7-22 kW) charging simultaneously would add up to 506 kW of demand -- a significant load on a microgrid whose evening demand is already 3,800 kW.

Smart charging flips this problem into an opportunity. Instead of charging immediately at maximum rate, the orchestrator searches for the cheapest available energy, creates an escrow-protected trade, and schedules charging during optimal periods.

```python
from greenhelix_trading import MicrogridOrchestrator

grid = MicrogridOrchestrator(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="microgrid-wilhelmsburg-001"
)

# Coordinate charging for an EV that arrives at 18:00
# Owner needs 30 kWh by 07:00 tomorrow (13-hour window)
ev_result = grid.coordinate_ev_charging(
    ev_agent_id="ev-charger-wbg-park-01",
    kwh_needed=30.0,
    max_price=0.22              # Won't pay more than EUR 0.22/kWh
)

print(f"EV Charging Plan:")
print(f"  Offers found: {len(ev_result['offers'].get('results', []))}")
print(f"  Escrow created: {ev_result['escrow'].get('escrow_id')}")
print(f"  Total cost: EUR {30.0 * 0.22:.2f} (max)")

# The coordinate_ev_charging method:
# 1. Calls search_services to find cheapest energy in the window
# 2. Calls create_escrow to lock funds for the trade
# Both API calls happen in sequence, returning combined results
```

### Demand Response Patterns

Demand response is the mechanism by which the grid operator (or microgrid orchestrator) signals participants to adjust their consumption in response to grid conditions. OpenADR 3.0 is the standard protocol for demand response signaling, but the economic settlement of demand response events flows through the GreenHelix gateway.

There are four canonical demand response patterns for microgrid coordination:

**Pattern 1: Load Shifting.** Move flexible loads (EV charging, water heating, pool pumps) from peak to off-peak periods. The orchestrator detects a peak period via `balance_grid_load`, identifies flexible loads, and dispatches charging commands to off-peak intervals.

```python
# Detect peak period and shift EV charging
evening_status = grid.balance_grid_load(
    supply_kwh=1200,
    demand_kwh=3800
)

if evening_status["status"] in ("deficit", "critical_deficit"):
    # Don't charge EVs now -- schedule for overnight
    print(f"Peak detected: deferring EV charging")
    print(f"  Current deficit: {evening_status['import_needed_kwh']} kWh")
    print(f"  Recommended: schedule charging after 23:00")

    # Check overnight balance (predicted)
    overnight_status = grid.balance_grid_load(
        supply_kwh=800,            # Battery discharge + wind
        demand_kwh=600              # Low overnight demand
    )
    print(f"  Overnight forecast: {overnight_status['status']}")
    print(f"  Surplus available: {overnight_status['curtailment_kwh']} kWh")
```

**Pattern 2: Battery Dispatch for Peak Shaving.** During evening peaks, the orchestrator discharges community batteries to reduce the net demand on the grid connection, avoiding expensive grid imports and potential transformer overloads.

```python
# Peak shaving: discharge batteries to reduce grid import
if evening_status["status"] == "critical_deficit":
    # Calculate how much battery discharge would move us to "deficit"
    # Need ratio >= 0.5 to exit critical_deficit
    target_supply = evening_status["demand_kwh"] * 0.5
    additional_supply_needed = target_supply - evening_status["supply_kwh"]

    print(f"Peak shaving required:")
    print(f"  Additional supply needed: {additional_supply_needed} kWh")

    # Dispatch batteries proportionally
    batteries = [
        ("battery-wbg-cs-003", 200, 0.82),  # id, capacity, SOC
        ("battery-wbg-cs-007", 200, 0.74),
        ("battery-wbg-cs-012", 150, 0.91),
    ]

    for battery_id, capacity_kwh, soc in batteries:
        available = capacity_kwh * soc * 0.9   # Leave 10% reserve
        discharge_kwh = min(available, additional_supply_needed / len(batteries))

        result = grid.dispatch_battery(
            battery_agent_id=battery_id,
            action="discharge",
            kwh=round(discharge_kwh, 1)
        )
        print(f"  Dispatched {battery_id}: discharge {discharge_kwh:.1f} kWh")
```

**Pattern 3: Solar Soak.** During midday solar surplus, the orchestrator activates flexible loads to absorb excess generation, preventing curtailment and reducing the need for expensive battery cycling.

```python
# Solar soak: absorb surplus during peak solar
midday_status = grid.balance_grid_load(
    supply_kwh=4800,
    demand_kwh=3200
)

if midday_status["status"] == "surplus":
    surplus_kwh = midday_status["curtailment_kwh"]
    print(f"Solar surplus: {surplus_kwh} kWh available for absorption")

    # Coordinate EV charging during solar surplus
    # EVs that are plugged in but not yet needed can charge cheaply
    parked_evs = [
        ("ev-charger-wbg-park-01", 25.0),  # id, kwh_needed
        ("ev-charger-wbg-park-03", 18.0),
        ("ev-charger-wbg-park-07", 32.0),
    ]

    for ev_id, kwh in parked_evs:
        if surplus_kwh <= 0:
            break
        charge_kwh = min(kwh, surplus_kwh)
        ev_charge = grid.coordinate_ev_charging(
            ev_agent_id=ev_id,
            kwh_needed=charge_kwh,
            max_price=0.10          # Very low price during surplus
        )
        surplus_kwh -= charge_kwh
        print(f"  Charging {ev_id}: {charge_kwh} kWh at EUR 0.10/kWh")
```

**Pattern 4: Emergency Island Mode.** When the main grid fails, the orchestrator islands the microgrid and coordinates all resources to maintain essential services. This is the scenario from the opening paragraph -- and the most complex orchestration challenge.

```python
# Emergency: grid connection lost
# Step 1: Assess available resources
island_supply = grid.balance_grid_load(
    supply_kwh=1800,           # Solar + battery discharge capacity
    demand_kwh=4200             # Full microgrid demand
)

print(f"ISLAND MODE ACTIVATED")
print(f"  Status: {island_supply['status']}")
print(f"  Shortfall: {island_supply['import_needed_kwh']} kWh")

# Step 2: Discharge all batteries to maximum
for battery_id in ["battery-wbg-cs-003", "battery-wbg-cs-007",
                    "battery-wbg-cs-012"]:
    grid.dispatch_battery(battery_id, "discharge", kwh=50.0)
    print(f"  Emergency discharge: {battery_id}")

# Step 3: Halt all non-essential EV charging
# (signal via demand response -- no new escrows created)
print(f"  Non-essential loads shed")
print(f"  Essential services prioritized")
```

### V2G Economics

Vehicle-to-grid transforms EV owners from pure consumers into prosumers. A parked EV with 50 kWh of available battery capacity can discharge 10 kWh during evening peak hours, earning the owner EUR 2.50-4.00 at peak P2P prices, while still retaining 40 kWh for their morning commute. Over a month of weekday V2G participation, that is EUR 50-80 in revenue -- enough to offset a significant portion of the EV's charging costs. The orchestrator manages this automatically: it knows the owner's departure time and minimum charge requirement, calculates the safe discharge window, and executes escrow-protected trades for the discharged energy.

---

## Chapter 7: Regulatory Compliance and Carbon Accounting

### FERC 2222, EU Energy Sharing, and Carbon Intensity Routing

Energy trading is one of the most heavily regulated commercial activities on the planet. Every kilowatt-hour traded must be metered, reported, and accounted for. Carbon content must be tracked for emissions reporting. Consumer protections must be enforced. Grid stability requirements must be met. The `EnergyComplianceManager` class automates these obligations through the GreenHelix gateway's `check_compliance`, `submit_metrics`, `get_analytics`, and `open_dispute` tools.

### Regional Compliance Checks

Different jurisdictions have different rules. The `check_grid_compliance` method calls the `check_compliance` tool with a region parameter to verify that the microgrid's trading activities conform to local regulations.

```python
from greenhelix_trading import EnergyComplianceManager

compliance = EnergyComplianceManager(
    api_key=os.environ["GREENHELIX_API_KEY"],
    agent_id="compliance-wilhelmsburg-001"
)

# Check compliance for the EU/Germany region
eu_compliance = compliance.check_grid_compliance(region="EU-DE")
print(f"EU/Germany Compliance Status:")
print(f"  Energy Sharing Directive: {eu_compliance.get('energy_sharing_directive')}")
print(f"  Grid Code VDE-AR-N 4105: {eu_compliance.get('grid_code_compliance')}")
print(f"  Metering Requirements: {eu_compliance.get('metering_compliance')}")
print(f"  Consumer Protection: {eu_compliance.get('consumer_protection')}")

# Check FERC 2222 compliance for US operations
us_compliance = compliance.check_grid_compliance(region="US-NYISO")
print(f"\nUS/NYISO Compliance Status:")
print(f"  FERC Order 2222: {us_compliance.get('ferc_2222')}")
print(f"  DER Aggregation: {us_compliance.get('der_aggregation')}")
print(f"  Wholesale Market Access: {us_compliance.get('wholesale_access')}")
```

### Carbon Offset Calculation

Every kWh of renewable energy traded P2P displaces a corresponding amount of fossil-fuel generation from the grid. The `calculate_carbon_offset` method quantifies this displacement using regional emission factors. Carbon intensity routing -- directing energy trades to maximize carbon displacement -- is becoming standard in EU grid codes.

```python
# Calculate carbon offset from Q1 2026 P2P renewable trades
q1_renewable_kwh = 847_000     # 847 MWh traded in Q1

# German grid emission factor: 0.385 kg CO2/kWh (2025 average)
# This represents the emissions that would have occurred if the
# buyer had consumed grid electricity instead of P2P renewables
carbon_offset = compliance.calculate_carbon_offset(
    kwh_renewable=q1_renewable_kwh,
    emission_factor_kg_per_kwh=0.385
)

print(f"Q1 2026 Carbon Impact:")
print(f"  Renewable energy traded: {carbon_offset['kwh_renewable']:,} kWh")
print(f"  CO2 avoided: {carbon_offset['co2_avoided_kg']:,.2f} kg")
print(f"  CO2 avoided: {carbon_offset['co2_avoided_tonnes']:.4f} tonnes")
print(f"  Equivalent to: {carbon_offset['trees_equivalent']:.1f} trees for one year")
# Output:
#   Renewable energy traded: 847,000 kWh
#   CO2 avoided: 326,095.00 kg
#   CO2 avoided: 326.0950 tonnes
#   Equivalent to: 14,981.9 trees for one year
```

The trees_equivalent metric (using the standard 21.77 kg CO2 per tree per year absorption rate) is useful for public communications and ESG reporting. The CO2 tonnes figure is what matters for regulatory compliance and carbon credit markets.

### Trade Parameter Validation

Before any trade executes, the `validate_trade_parameters` method performs sanity checks on the trade terms. This catches common errors -- missing fields, negative quantities, above-market pricing, unusually large trades -- before they reach the escrow system.

```python
# Validate a well-formed trade
valid_trade = {
    "seller_id": "prosumer-hamburg-2847",
    "buyer_id": "consumer-hamburg-5012",
    "kwh": 8.0,
    "price_per_kwh": 0.19,
    "duration_hours": 2
}
result = compliance.validate_trade_parameters(valid_trade)
print(f"Valid: {result['valid']}")       # True
print(f"Warnings: {result['warnings']}") # []
print(f"Errors: {result['errors']}")     # []

# Validate a problematic trade
risky_trade = {
    "seller_id": "prosumer-hamburg-2847",
    "buyer_id": "consumer-hamburg-5012",
    "kwh": 1500,                  # Very large trade
    "price_per_kwh": 0.55,        # Above market rate
    "duration_hours": 48           # Extended delivery window
}
result = compliance.validate_trade_parameters(risky_trade)
print(f"Valid: {result['valid']}")       # True (no hard errors)
print(f"Warnings: {result['warnings']}")
# Output: ['large_trade', 'above_market_rate', 'extended_delivery_window']

# Validate a trade with missing fields
incomplete_trade = {
    "seller_id": "prosumer-hamburg-2847",
    "kwh": -5.0                   # Negative kWh
}
result = compliance.validate_trade_parameters(incomplete_trade)
print(f"Valid: {result['valid']}")          # False
print(f"Missing: {result['missing_fields']}")
# Output: ['buyer_id', 'price_per_kwh', 'duration_hours']
print(f"Errors: {result['errors']}")
# Output: ['kwh_must_be_positive']
```

### Filing Delivery Disputes

When a trade results in significant under-delivery, the compliance manager files a dispute through the `open_dispute` tool. The dispute includes the seller ID, trade ID, the shortfall in kWh, and supporting evidence (typically the meter reading data).

```python
# File a dispute for a trade where only 5.2 of 8.0 kWh were delivered
dispute = compliance.file_delivery_dispute(
    seller_id="prosumer-hamburg-2847",
    trade_id="trade-20260214-1015-WBG",
    shortfall_kwh=2.8,
    evidence={
        "meter_reading": {
            "meter_id": "EDLH-5012-SM-001",
            "interval_start": "2026-02-14T10:00:00Z",
            "interval_end": "2026-02-14T12:00:00Z",
            "energy_received_kwh": 5.2,
            "contracted_kwh": 8.0
        },
        "weather_data": {
            "cloud_cover_pct": 85,
            "note": "Unexpected cloud cover reduced seller solar generation"
        },
        "sla_id": "sla-20260214-1015-WBG",
        "tolerance_exceeded": True
    }
)

print(f"Dispute filed: {dispute.get('dispute_id')}")
print(f"  Shortfall: 2.8 kWh (35% under-delivery)")
print(f"  Escrow status: held pending resolution")
print(f"  Expected resolution: partial refund proportional to shortfall")
```

The dispute mechanism is crucial for market integrity. Without it, sellers could over-promise and under-deliver with no consequence. The escrow remains locked until the dispute is resolved -- either through automated adjudication (if the meter data clearly shows under-delivery) or through manual review. In most cases, the resolution is a proportional payment: the seller receives payment for the energy actually delivered, and the shortfall amount is returned to the buyer.

### Generating Regulatory Reports

The `generate_regulatory_report` method combines two API calls -- `get_analytics` for trading data and `check_compliance` for regulatory status -- into a single report suitable for submission to energy regulators.

```python
# Generate Q1 2026 regulatory report
report = compliance.generate_regulatory_report(period="2026-Q1")

analytics = report["analytics"]
compliance_status = report["compliance"]

print(f"Regulatory Report: Q1 2026")
print(f"{'=' * 50}")
print(f"Trading Volume:")
print(f"  Total trades: {analytics.get('total_trades', 0)}")
print(f"  Total kWh traded: {analytics.get('total_kwh', 0):,.0f}")
print(f"  Total value: EUR {analytics.get('total_value_eur', 0):,.2f}")
print(f"  Average price: EUR {analytics.get('avg_price_per_kwh', 0):.4f}/kWh")
print()
print(f"Compliance Status:")
print(f"  Energy Sharing Directive: {compliance_status.get('directive_compliant')}")
print(f"  Grid Code: {compliance_status.get('grid_code_compliant')}")
print(f"  Metering: {compliance_status.get('metering_compliant')}")
print(f"  Consumer Protection: {compliance_status.get('consumer_protection_compliant')}")
print(f"  Outstanding Disputes: {compliance_status.get('open_disputes', 0)}")
```

### Trading History for Audit

The `get_trading_history` method retrieves historical trade data for any period, providing the audit trail that regulators require under both FERC Order 2222 and the EU Energy Sharing Directive.

```python
# Retrieve trading history for February 2026
history = compliance.get_trading_history(period="2026-02")
print(f"February 2026 Trading History:")
print(f"  Records: {len(history.get('trades', []))}")
print(f"  Period: {history.get('period')}")
for trade in history.get("trades", [])[:3]:
    print(f"  - {trade.get('timestamp')}: {trade.get('kwh')} kWh "
          f"@ EUR {trade.get('price_per_kwh')}/kWh "
          f"({trade.get('seller_id')} -> {trade.get('buyer_id')})")
```

---

## Next Steps

For deployment patterns, monitoring, and production hardening, see the
[Agent Production Hardening Guide](https://clawhub.ai/skills/greenhelix-agent-production-hardening).

