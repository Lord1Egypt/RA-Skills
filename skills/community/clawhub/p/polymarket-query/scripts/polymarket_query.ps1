<#
.SYNOPSIS
Polymarket Real-time Query Tool (PowerShell version)
Query markets, events, odds, and live data from Polymarket's public APIs.

.EXAMPLE
.\polymarket_query.ps1 categories
.\polymarket_query.ps1 trending -Limit 10
.\polymarket_query.ps1 search -Keyword "Trump"
.\polymarket_query.ps1 market -Id 540816
.\polymarket_query.ps1 event -Id 320112
.\polymarket_query.ps1 odds -Id 540816
.\polymarket_query.ps1 sports -Limit 15
.\polymarket_query.ps1 politics
.\polymarket_query.ps1 crypto
.\polymarket_query.ps1 category -Slug basketball
.\polymarket_query.ps1 live
.\polymarket_query.ps1 schedule -Sport nba -Date 2026-04-12
.\polymarket_query.ps1 schedule -Sport soccer -Date 2026-04-11
#>

param(
    [Parameter(Position=0)]
    [string]$Command = "",

    [string]$Keyword = "",
    [string]$Id = "",
    [string]$Slug = "",
    [string]$Sport = "",
    [string]$Date = "",
    [int]$Limit = 10
)

$ErrorActionPreference = "SilentlyContinue"
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$GAMMA_API = "https://gamma-api.polymarket.com"

function Fetch-Json {
    param([string]$Url)
    try {
        $resp = Invoke-WebRequest -Uri $Url -TimeoutSec 25 -UseBasicParsing -Headers @{
            "User-Agent" = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "Accept" = "application/json"
        }
        return $resp.Content | ConvertFrom-Json
    } catch {
        Write-Host "Error fetching $Url : $_" -ForegroundColor Red
        return $null
    }
}

function Format-Price {
    param([string]$PriceStr)
    try {
        $p = [double]$PriceStr
        return "{0:N1}%" -f ($p * 100)
    } catch { return $PriceStr }
}

function Format-Volume {
    param($Vol)
    try {
        $v = [double]$Vol
        if ($v -ge 1000000) { return "`${0:N2}M" -f ($v / 1000000) }
        elseif ($v -ge 1000) { return "`${0:N1}K" -f ($v / 1000) }
        else { return "`${0:N2}" -f $v }
    } catch { return "$Vol" }
}

function Show-Categories {
    $data = Fetch-Json "$GAMMA_API/categories?limit=100"
    if (-not $data) { return }

    $parents = @{}
    $children = @{}
    foreach ($cat in $data) {
        $pc = $cat.parentCategory
        if (-not $pc -or $pc -eq "") {
            $parents[$cat.id] = $cat
        } else {
            if (-not $children.ContainsKey($pc)) {
                $children[$pc] = @()
            }
            $children[$pc] += $cat
        }
    }

    Write-Host ("=" * 60)
    Write-Host "POLYMARKET CATEGORIES"
    Write-Host ("=" * 60)

    $sortedParents = $parents.Values | Sort-Object { if ($_.label) { $_.label } else { "" } }
    foreach ($p in $sortedParents) {
        $pid = $p.id
        Write-Host ""
        Write-Host "  $($p.label) (slug: $($p.slug))" -ForegroundColor Cyan
        if ($children.ContainsKey($pid)) {
            $sortedChildren = $children[$pid] | Sort-Object { if ($_.label) { $_.label } else { "" } }
            foreach ($child in $sortedChildren) {
                Write-Host "    -> $($child.label) (slug: $($child.slug))"
            }
        }
    }
}

function Show-Markets {
    param([string]$Title, [string]$Url, [int]$Count = 10)

    $data = Fetch-Json $Url
    if (-not $data) { return }

    Write-Host ("=" * 80)
    Write-Host $Title -ForegroundColor Yellow
    Write-Host ("=" * 80)

    $i = 0
    foreach ($m in $data) {
        $i++
        Write-Host ""
        Write-Host "$i. $($m.question)" -ForegroundColor White
        Write-Host "   ID: $($m.id)"

        try {
            $outcomes = $m.outcomes | ConvertFrom-Json
            $prices = $m.outcomePrices | ConvertFrom-Json
            for ($j = 0; $j -lt $outcomes.Count; $j++) {
                $o = $outcomes[$j]
                $p = Format-Price $prices[$j]
                Write-Host "   ${o}: $p" -ForegroundColor Green
            }
        } catch {}

        $vol24 = Format-Volume $m.volume24hr
        $volTotal = Format-Volume $m.volumeNum
        $liq = Format-Volume $m.liquidityNum
        Write-Host "   Vol 24h: $vol24 | Total: $volTotal | Liquidity: $liq" -ForegroundColor Gray
        Write-Host "   End: $($m.endDateIso)  |  URL: https://polymarket.com/event/$($m.slug)" -ForegroundColor DarkGray
    }
}

function Show-MarketDetail {
    param([string]$MarketId)

    $m = Fetch-Json "$GAMMA_API/markets/$MarketId"
    if (-not $m) { return }

    Write-Host ("=" * 80)
    Write-Host "MARKET DETAILS" -ForegroundColor Yellow
    Write-Host ("=" * 80)
    Write-Host "Question: $($m.question)" -ForegroundColor White
    Write-Host "ID: $($m.id)"
    Write-Host "Slug: $($m.slug)"

    $desc = $m.description
    if ($desc.Length -gt 500) { $desc = $desc.Substring(0, 500) + "..." }
    Write-Host ""
    Write-Host "Description:" -ForegroundColor Cyan
    Write-Host "  $desc"

    Write-Host ""
    Write-Host "ODDS / PRICES:" -ForegroundColor Cyan
    try {
        $outcomes = $m.outcomes | ConvertFrom-Json
        $prices = $m.outcomePrices | ConvertFrom-Json
        for ($j = 0; $j -lt $outcomes.Count; $j++) {
            $o = $outcomes[$j]
            $p = Format-Price $prices[$j]
            $pd = [double]$prices[$j]
            if ($pd -gt 0) {
                $implied = "{0:N1}x" -f (1 / $pd)
                Write-Host "  ${o}: $p (implied: $implied)"
            } else {
                Write-Host "  ${o}: $p"
            }
        }
    } catch {}

    Write-Host ""
    Write-Host "PRICE CHANGES:" -ForegroundColor Cyan
    foreach ($pair in @(@("1 Day","oneDayPriceChange"), @("1 Week","oneWeekPriceChange"), @("1 Month","oneMonthPriceChange"))) {
        $val = $m.($pair[1])
        if ($null -ne $val) {
            $vd = [double]$val
            $arrow = if ($vd -gt 0) { "[+]" } elseif ($vd -lt 0) { "[-]" } else { "[=]" }
            Write-Host ("  {0}: {1} {2:N2}%" -f $pair[0], $arrow, ($vd * 100))
        }
    }

    Write-Host ""
    Write-Host "VOLUME & LIQUIDITY:" -ForegroundColor Cyan
    Write-Host "  24h Volume:   $(Format-Volume $m.volume24hr)"
    Write-Host "  1wk Volume:   $(Format-Volume $m.volume1wk)"
    Write-Host "  Total Volume: $(Format-Volume $m.volumeNum)"
    Write-Host "  Liquidity:    $(Format-Volume $m.liquidityNum)"
    Write-Host "  Open Interest:$(Format-Volume $m.openInterest)"

    Write-Host ""
    Write-Host "DATES:" -ForegroundColor Cyan
    Write-Host "  Start: $($m.startDateIso)"
    Write-Host "  End:   $($m.endDateIso)"

    Write-Host ""
    Write-Host "STATUS:" -ForegroundColor Cyan
    Write-Host "  Active: $($m.active) | Closed: $($m.closed) | Accepting Orders: $($m.acceptingOrders)"
    if ($m.gameStartTime) { Write-Host "  Game Start: $($m.gameStartTime)" }

    Write-Host ""
    Write-Host "URL: https://polymarket.com/event/$($m.slug)" -ForegroundColor Blue
}

function Show-Event {
    param([string]$EventId)

    $e = Fetch-Json "$GAMMA_API/events/$EventId"
    if (-not $e) { return }

    Write-Host ("=" * 80)
    Write-Host "EVENT: $($e.title)" -ForegroundColor Yellow
    Write-Host ("=" * 80)
    Write-Host "ID: $($e.id)"
    Write-Host "Slug: $($e.slug)"

    $desc = $e.description
    if ($desc.Length -gt 300) { $desc = $desc.Substring(0, 300) + "..." }
    Write-Host "Description: $desc"

    Write-Host ""
    Write-Host "Volume: $(Format-Volume $e.volume) | Liquidity: $(Format-Volume $e.liquidity) | Open Interest: $(Format-Volume $e.openInterest)"
    Write-Host "24h Volume: $(Format-Volume $e.volume24hr)"

    $markets = $e.markets
    if ($markets) {
        Write-Host ""
        Write-Host "SUB-MARKETS ($($markets.Count)):" -ForegroundColor Cyan
        Write-Host ("-" * 80)
        $i = 0
        foreach ($m in $markets) {
            $i++
            Write-Host ""
            Write-Host "  $i. $($m.question)"
            Write-Host "     ID: $($m.id)"
            try {
                $outcomes = $m.outcomes | ConvertFrom-Json
                $prices = $m.outcomePrices | ConvertFrom-Json
                for ($j = 0; $j -lt $outcomes.Count; $j++) {
                    Write-Host "     $($outcomes[$j]): $(Format-Price $prices[$j])"
                }
            } catch {}
            Write-Host "     Vol: $(Format-Volume $m.volume) | Closed: $($m.closed)" -ForegroundColor Gray
        }
    }

    Write-Host ""
    Write-Host "URL: https://polymarket.com/event/$($e.slug)" -ForegroundColor Blue
}

function Show-Odds {
    param([string]$MarketId)

    $m = Fetch-Json "$GAMMA_API/markets/$MarketId"
    if (-not $m) { return }

    Write-Host ("=" * 60)
    Write-Host "ODDS: $($m.question)" -ForegroundColor Yellow
    Write-Host ("=" * 60)

    try {
        $outcomes = $m.outcomes | ConvertFrom-Json
        $prices = $m.outcomePrices | ConvertFrom-Json
        Write-Host ""
        Write-Host ("{0,-20} {1,10} {2,10} {3,10}" -f "Outcome", "Price", "Odds", "Implied")
        Write-Host ("-" * 55)
        for ($j = 0; $j -lt $outcomes.Count; $j++) {
            $pd = [double]$prices[$j]
            $implied = if ($pd -gt 0) { "{0:N1}x" -f (1 / $pd) } else { "N/A" }
            Write-Host ("{0,-20} {1,10} {2,10} {3,10}" -f $outcomes[$j], (Format-Price $prices[$j]), $implied, (Format-Price $prices[$j]))
        }
    } catch {}

    if ($null -ne $m.lastTradePrice) { Write-Host "`nLast Trade: $(Format-Price $m.lastTradePrice)" }
    if ($null -ne $m.bestBid) { Write-Host "Best Bid: $(Format-Price $m.bestBid)" }
    if ($null -ne $m.bestAsk) { Write-Host "Best Ask: $(Format-Price $m.bestAsk)" }
    if ($null -ne $m.spread) { Write-Host "Spread: {0:N2}%" -f ([double]$m.spread * 100) }

    Write-Host "`nPrice Changes:" -ForegroundColor Cyan
    foreach ($pair in @(@("1D","oneDayPriceChange"), @("1W","oneWeekPriceChange"), @("1M","oneMonthPriceChange"))) {
        $val = $m.($pair[1])
        if ($null -ne $val) {
            $vd = [double]$val
            $color = if ($vd -gt 0) { "Green" } elseif ($vd -lt 0) { "Red" } else { "Gray" }
            Write-Host ("  {0}: {1:N2}%" -f $pair[0], ($vd * 100)) -ForegroundColor $color
        }
    }
}

function Show-Live {
    $data = Fetch-Json "$GAMMA_API/markets?limit=50&active=true&closed=false&order=volume24hr&ascending=false&category=sports"
    if (-not $data) { return }

    $now = [DateTime]::UtcNow
    $liveMarkets = @()

    foreach ($m in $data) {
        if ($m.gameStartTime) {
            try {
                $gs = [DateTime]::Parse($m.gameStartTime.Replace("+00", "").Replace("+0000", ""))
                $diff = ($now - $gs).TotalSeconds
                if ($diff -gt -3600 -and $diff -lt 10800) {
                    $liveMarkets += ,@($m, $gs, $diff)
                }
            } catch {}
        }
    }

    if ($liveMarkets.Count -eq 0) {
        Write-Host "No live/in-play markets found at the moment." -ForegroundColor Yellow
        Write-Host "Showing upcoming sports markets instead:" -ForegroundColor Gray
        Show-Markets -Title "SPORTS MARKETS" -Url "$GAMMA_API/markets?limit=$Limit&active=true&closed=false&order=volume24hr&ascending=false&category=sports" -Count $Limit
        return
    }

    Write-Host ("=" * 80)
    Write-Host "LIVE / IN-PLAY MARKETS ($($liveMarkets.Count) found)" -ForegroundColor Red
    Write-Host ("=" * 80)

    $i = 0
    foreach ($item in $liveMarkets) {
        $m = $item[0]
        $gs = $item[1]
        $diff = $item[2]
        $i++

        $status = if ($diff -gt 0) { "LIVE" } else { "STARTING SOON" }
        Write-Host ""
        Write-Host "$i. [$status] $($m.question)" -ForegroundColor White
        Write-Host "   ID: $($m.id)"
        Write-Host "   Game Start: $($m.gameStartTime)"

        try {
            $outcomes = $m.outcomes | ConvertFrom-Json
            $prices = $m.outcomePrices | ConvertFrom-Json
            for ($j = 0; $j -lt $outcomes.Count; $j++) {
                Write-Host "   $($outcomes[$j]): $(Format-Price $prices[$j])" -ForegroundColor Green
            }
        } catch {}

        Write-Host "   Vol 24h: $(Format-Volume $m.volume24hr)" -ForegroundColor Gray
    }
}

function Show-Schedule {
    param([string]$Sport, [string]$DateStr, [int]$Limit = 50)

    # Normalize sport name to slug prefix(es) used by Polymarket
    # Game events use short prefixes (e.g. "lal", "epl"), while season/award
    # events may use longer prefixes (e.g. "la-liga", "english-premier-league").
    $sportMap = @{
        "nba" = @("nba"); "basketball" = @("nba");
        "nfl" = @("nfl"); "football" = @("nfl");
        "mlb" = @("mlb"); "baseball" = @("mlb");
        "nhl" = @("nhl"); "hockey" = @("nhl");
        "soccer" = @("epl", "lal", "serie", "bundes", "ligue");
        "epl" = @("epl"); "premier" = @("epl"); "premierleague" = @("epl", "english-premier-league");
        "la_liga" = @("lal", "la-liga"); "laliga" = @("lal", "la-liga");
        "ligue1" = @("ligue-1", "l1"); "seriea" = @("serie", "serie-a");
        "bundesliga" = @("bundes", "bundesliga");
        "champions" = @("ucl"); "ucl" = @("ucl"); "championsleague" = @("ucl");
        "mls" = @("mls"); "tennis" = @("atp"); "atp" = @("atp"); "wta" = @("wta");
        "mma" = @("ufc"); "ufc" = @("ufc"); "cs2" = @("cs2"); "csgo" = @("cs2");
        "counterstrike" = @("cs2"); "lol" = @("lol"); "leagueoflegends" = @("lol");
        "f1" = @("f1"); "racing" = @("f1"); "golf" = @("pga"); "pga" = @("pga");
        "boxing" = @("boxing"); "cricket" = @("cricket")
    }

    $slugPrefixes = @()
    if ($Sport) {
        $sp = $Sport.ToLower().Trim()
        if ($sportMap.ContainsKey($sp)) { $slugPrefixes = @($sportMap[$sp]) } else { $slugPrefixes = @($sp) }
    }

    # Normalize date
    $dateFilter = ""
    if ($DateStr) {
        $dateFilter = $DateStr.Trim() -replace "/", "-"
    }

    $header = "SPORTS SCHEDULE"
    if ($Sport) { $header += " - $($Sport.ToUpper())" }
    if ($dateFilter) { $header += " - $dateFilter" }
    Write-Host ("=" * 80)
    Write-Host $header -ForegroundColor Yellow
    Write-Host ("=" * 80)

    # Strategy: Fetch /events by volume, filter by slug prefix client-side
    # The Polymarket API's tag/search/filter parameters are unreliable.
    # Sport game events appear in the top events by volume, so we iterate
    # and filter by slug prefix (e.g. "nba-xxx-yyy-date") on the client side.
    $filtered = @()

    if ($slugPrefixes.Count -gt 0) {
        $seenSlugs = @{}
        $rawEvents = @()

        # Iterate /events by volume, filter by slug prefixes
        foreach ($slugPrefix in $slugPrefixes) {
            $offset = 0
            $maxPages = 10
            while ($offset -lt $maxPages * 100) {
                $fetchUrl = "$GAMMA_API/events?limit=100&active=true&closed=false&order=volume24hr&ascending=false&offset=$offset"
                $batch = Fetch-Json $fetchUrl
                if (-not $batch -or $batch.Count -eq 0) { break }
                $foundInBatch = 0
                foreach ($e in $batch) {
                    $slug = if ($e.slug) { $e.slug } else { "" }
                    if ($slug.StartsWith("$slugPrefix-") -and -not $seenSlugs.ContainsKey($slug)) {
                        $seenSlugs[$slug] = $true
                        $rawEvents += $e
                        $foundInBatch++
                    }
                }
                if ($batch.Count -lt 100) { break }
                # Optimization: if no matches found and we're past page 2, stop
                if ($foundInBatch -eq 0 -and $offset -ge 200) { break }
                $offset += 100
            }
        }

        # Filter by date and normalize event data
        foreach ($ev in $rawEvents) {
            $slug = if ($ev.slug) { $ev.slug.ToLower() } else { "" }
            $title = if ($ev.title) { $ev.title.ToLower() } else { "" }
            $endDate = ""
            $startDate = ""
            if ($ev.endDate -and $ev.endDate.Length -ge 10) { $endDate = $ev.endDate.Substring(0, 10) }
            if ($ev.startDate -and $ev.startDate.Length -ge 10) { $startDate = $ev.startDate.Substring(0, 10) }
            $gameTime = if ($ev.gameStartTime) { $ev.gameStartTime } else { "" }

            # Determine if this is a "game" event (slug contains date like 2026-04-12)
            # vs an "award" event (slug like nba-mvp-694 or la-liga-winner-114)
            # Try matching against any of the slug prefixes
            # Note: team abbreviations may contain digits (e.g. lol-ig1, ucl-liv1, ufc-cur1)
            $isGame = $false
            foreach ($pfx in $slugPrefixes) {
                if ($slug -match "^$pfx-[a-z0-9]+-[a-z0-9]+-\d{4}-\d{2}-\d{2}") {
                    $isGame = $true
                    break
                }
            }
            # Special case: boxing/fighting events don't follow the team-date slug pattern;
            # their slugs look like "boxing-fighter1-vs-fighter2" (no date in slug)
            # Treat them as game events regardless of gameStartTime
            if (-not $isGame) {
                foreach ($pfx in $slugPrefixes) {
                    if ($slug.StartsWith("$pfx-") -and $slug.Contains("-vs-")) {
                        $isGame = $true
                        break
                    }
                }
            }

            $dateMatch = $true
            if ($dateFilter) {
                if ($isGame) {
                    # For game events: match date in slug, endDate, startDate, or gameStartTime
                    $dateMatch = $slug.Contains($dateFilter) -or ($endDate -eq $dateFilter) -or ($startDate -eq $dateFilter) -or $gameTime.Contains($dateFilter)
                } else {
                    # For award/season events: skip when date filter is specified
                    # (schedule command is for game schedules, not awards)
                    $dateMatch = $false
                }
            }

            if ($dateMatch) {
                # Build title from slug if needed
                $dispTitle = if ($ev.title) { $ev.title } else { "N/A" }
                if ($dispTitle -eq "N/A" -or -not $dispTitle) {
                    $slugParts = $slug.Split("-")
                    if ($slugParts.Length -ge 3) {
                        $dispTitle = "$($slugParts[1].ToUpper()) vs $($slugParts[2].ToUpper())"
                    }
                }

                # Get markets
                $markets = @()
                if ($ev.markets) {
                    $markets = @($ev.markets)
                } else {
                    $eventId = $ev.id
                    if ($eventId) {
                        $mUrl = "$GAMMA_API/markets?limit=20&event_id=$eventId"
                        $mData = Fetch-Json $mUrl
                        if ($mData -and $mData.Count -gt 0) { $markets = $mData }
                    }
                }

                $filtered += @{
                    id = $ev.id
                    title = $dispTitle
                    slug = $slug
                    gameStartTime = $gameTime
                    endDate = $endDate
                    startDate = $startDate
                    volume = [double]($ev.volume)
                    volume24hr = [double]($ev.volume24hr)
                    openInterest = [double]($ev.openInterest)
                    markets = $markets
                }
            }
        }
    } else {
        # No sport specified - fetch all sports markets
        $allMarkets = @()
        $offset = 0
        while ($offset -lt 300) {
            $fetchUrl = "$GAMMA_API/markets?limit=100&active=true&closed=false&order=volume24hr&ascending=false&tag=sports&offset=$offset"
            $batch = Fetch-Json $fetchUrl
            if (-not $batch -or $batch.Count -eq 0) { break }
            $allMarkets += $batch
            if ($batch.Count -lt 100) { break }
            $offset += 100
        }

        # Group by slug prefix
        $eventsMap = @{}
        foreach ($m in $allMarkets) {
            $slug = if ($m.slug) { $m.slug } else { "" }
            $lastDash = $slug.LastIndexOf("-")
            $eventKey = if ($lastDash -gt 0) { $slug.Substring(0, $lastDash) } else { $slug }

            if (-not $eventsMap.ContainsKey($eventKey)) {
                $eventsMap[$eventKey] = @{
                    id = $m.id
                    title = if ($m.groupItemTitle) { $m.groupItemTitle } else { $m.question }
                    slug = $eventKey
                    markets = @()
                    gameStartTime = ""
                    endDate = ""
                    startDate = ""
                    volume = 0
                    volume24hr = 0
                    openInterest = 0
                }
            }
            $eventsMap[$eventKey].markets += $m
            try { $eventsMap[$eventKey].volume += [double]($m.volume) } catch {}
            try { $eventsMap[$eventKey].volume24hr += [double]($m.volume24hr) } catch {}
            try { $eventsMap[$eventKey].openInterest += [double]($m.openInterest) } catch {}
            if ($m.gameStartTime) {
                if (-not $eventsMap[$eventKey].gameStartTime -or $m.gameStartTime -lt $eventsMap[$eventKey].gameStartTime) {
                    $eventsMap[$eventKey].gameStartTime = $m.gameStartTime
                }
            }
            $endRaw = if ($m.endDateIso) { $m.endDateIso } elseif ($m.endDate) { $m.endDate } else { "" }
            $startRaw = if ($m.startDateIso) { $m.startDateIso } elseif ($m.startDate) { $m.startDate } else { "" }
            if ($endRaw -and -not $eventsMap[$eventKey].endDate -and $endRaw.Length -ge 10) {
                $eventsMap[$eventKey].endDate = $endRaw.Substring(0, 10)
            }
            if ($startRaw -and -not $eventsMap[$eventKey].startDate -and $startRaw.Length -ge 10) {
                $eventsMap[$eventKey].startDate = $startRaw.Substring(0, 10)
            }
        }

        # Filter by date
        foreach ($key in $eventsMap.Keys) {
            $ev = $eventsMap[$key]
            $slug = if ($ev.slug) { $ev.slug.ToLower() } else { "" }
            $endDate = if ($ev.endDate) { $ev.endDate } else { "" }
            $startDate = if ($ev.startDate) { $ev.startDate } else { "" }
            $dateMatch = $true
            if ($dateFilter) {
                $gameTimeStr = if ($ev.gameStartTime) { $ev.gameStartTime } else { "" }
                $dateMatch = ($endDate -eq $dateFilter) -or ($startDate -eq $dateFilter) -or $slug.Contains($dateFilter) -or $gameTimeStr.Contains($dateFilter)
            }
            if ($dateMatch) {
                $filtered += $ev
            }
        }
    }

    if ($filtered.Count -eq 0) {
        Write-Host ""
        Write-Host "No events found" -ForegroundColor Yellow
        if ($Sport) { Write-Host "  Sport: $Sport" }
        if ($dateFilter) { Write-Host "  Date: $dateFilter" }
        Write-Host ""
        Write-Host "Supported sport keywords:" -ForegroundColor Gray
        Write-Host "  nba, nfl, mlb, nhl, soccer/epl, atp/tennis, ufc/mma, cs2, lol, f1, pga/golf, boxing" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Tip: Try without date to see all upcoming $($Sport.ToUpper()) events" -ForegroundColor Gray
        return
    }

    # Sort by game start time
    $filtered = $filtered | Sort-Object { if ($_.gameStartTime) { $_.gameStartTime } elseif ($_.startDate) { $_.startDate } else { "zzz" } }

    Write-Host ""
    Write-Host "Found $($filtered.Count) event(s):" -ForegroundColor Cyan

    foreach ($ev in $filtered) {
        Write-Host ""
        Write-Host "  $($ev.title)" -ForegroundColor White
        Write-Host "  Slug: $($ev.slug) | Event ID: $($ev.id)" -ForegroundColor DarkGray

        if ($ev.gameStartTime) {
            Write-Host "  Game Time: $($ev.gameStartTime)" -ForegroundColor Cyan
        }

        Write-Host "  Volume: $(Format-Volume $ev.volume) | 24h Vol: $(Format-Volume $ev.volume24hr) | OI: $(Format-Volume $ev.openInterest)" -ForegroundColor Gray

        # Show sub-markets with odds
        foreach ($m in $ev.markets) {
            Write-Host ""
            Write-Host "    [$($m.question)]" -ForegroundColor Yellow
            try {
                $outcomes = $m.outcomes | ConvertFrom-Json
                $prices = $m.outcomePrices | ConvertFrom-Json
                for ($j = 0; $j -lt $outcomes.Count; $j++) {
                    Write-Host "      $($outcomes[$j]): $(Format-Price $prices[$j])" -ForegroundColor Green
                }
            } catch {}
            if ($m.spread) {
                try { Write-Host "      Spread: {0:N2}%" -f ([double]$m.spread * 100) -ForegroundColor DarkGray } catch {}
            }
        }

        Write-Host ""
        Write-Host "  URL: https://polymarket.com/event/$($ev.slug)" -ForegroundColor Blue
        Write-Host "  $('-' * 70)" -ForegroundColor DarkGray
    }
}

function Show-Search {
    param([string]$Keyword, [int]$Limit = 10)

    $keywordLower = $Keyword.ToLower()

    # Fetch a large set of active markets and filter by keyword
    $data = Fetch-Json "$GAMMA_API/markets?limit=100&active=true&closed=false&order=volume24hr&ascending=false"
    if (-not $data) { Write-Host "Error fetching markets."; return }

    $filtered = @()
    foreach ($m in $data) {
        $q = if ($m.question) { $m.question.ToLower() } else { "" }
        $d = if ($m.description) { $m.description.ToLower() } else { "" }
        if ($q.Contains($keywordLower) -or $d.Contains($keywordLower)) {
            $filtered += $m
        }
        if ($filtered.Count -ge $Limit) { break }
    }

    $data = $filtered

    if (-not $data -or $data.Count -eq 0) {
        Write-Host "No markets found for '$Keyword'" -ForegroundColor Yellow
        return
    }

    Write-Host ("=" * 80)
    Write-Host "SEARCH RESULTS: '$Keyword' ($($data.Count) results)" -ForegroundColor Yellow
    Write-Host ("=" * 80)

    $i = 0
    foreach ($m in $data) {
        $i++
        Write-Host ""
        Write-Host "$i. $($m.question)" -ForegroundColor White
        Write-Host "   ID: $($m.id)"
        try {
            $outcomes = $m.outcomes | ConvertFrom-Json
            $prices = $m.outcomePrices | ConvertFrom-Json
            for ($j = 0; $j -lt $outcomes.Count; $j++) {
                Write-Host "   $($outcomes[$j]): $(Format-Price $prices[$j])" -ForegroundColor Green
            }
        } catch {}
        Write-Host "   Vol 24h: $(Format-Volume $m.volume24hr) | Total: $(Format-Volume $m.volumeNum)" -ForegroundColor Gray
        Write-Host "   End: $($m.endDateIso)" -ForegroundColor DarkGray
    }
}

# Main dispatch
switch ($Command.ToLower()) {
    "categories" { Show-Categories }
    "trending"   { Show-Markets -Title "TRENDING MARKETS (Top $Limit by 24h Volume)" -Url "$GAMMA_API/markets?limit=$Limit&active=true&closed=false&order=volume24hr&ascending=false" -Count $Limit }
    "search"     { if (-not $Keyword) { Write-Host "Usage: -Command search -Keyword <keyword>"; return }; Show-Search -Keyword $Keyword -Limit $Limit }
    "market"     { if (-not $Id) { Write-Host "Usage: -Command market -Id <market_id>"; return }; Show-MarketDetail -MarketId $Id }
    "event"      { if (-not $Id) { Write-Host "Usage: -Command event -Id <event_id>"; return }; Show-Event -EventId $Id }
    "odds"       { if (-not $Id) { Write-Host "Usage: -Command odds -Id <market_id>"; return }; Show-Odds -MarketId $Id }
    "sports"     { Show-Markets -Title "SPORTS MARKETS" -Url "$GAMMA_API/markets?limit=$Limit&active=true&closed=false&order=volume24hr&ascending=false&category=sports" -Count $Limit }
    "politics"   { Show-Markets -Title "POLITICS MARKETS" -Url "$GAMMA_API/markets?limit=$Limit&active=true&closed=false&order=volume24hr&ascending=false&category=politics" -Count $Limit }
    "crypto"     { Show-Markets -Title "CRYPTO MARKETS" -Url "$GAMMA_API/markets?limit=$Limit&active=true&closed=false&order=volume24hr&ascending=false&category=crypto" -Count $Limit }
    "category"   { if (-not $Slug) { Write-Host "Usage: -Command category -Slug <slug>"; return }; Show-Markets -Title "CATEGORY: $Slug".ToUpper() -Url "$GAMMA_API/markets?limit=$Limit&active=true&closed=false&order=volume24hr&ascending=false&category=$Slug" -Count $Limit }
    "live"       { Show-Live }
    "schedule"   { Show-Schedule -Sport $Sport -DateStr $Date -Limit $Limit }
    default {
        Write-Host "Polymarket Real-time Query Tool" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "Usage:" -ForegroundColor Yellow
        Write-Host "  .\polymarket_query.ps1 -Command <command> [options]"
        Write-Host ""
        Write-Host "Commands:" -ForegroundColor Yellow
        Write-Host "  categories               List all market categories"
        Write-Host "  trending   [-Limit N]    Show trending markets (default N=10)"
        Write-Host "  search     -Keyword X    Search markets by keyword"
        Write-Host "  market     -Id X         Get detailed market info"
        Write-Host "  event      -Id X         Get event with sub-markets"
        Write-Host "  odds       -Id X         Get odds for a market"
        Write-Host "  sports     [-Limit N]    Show sports markets"
        Write-Host "  politics   [-Limit N]    Show politics markets"
        Write-Host "  crypto     [-Limit N]    Show crypto markets"
        Write-Host "  category   -Slug X       Markets in a category"
        Write-Host "  live                     Show live/in-play markets"
        Write-Host "  schedule   [-Sport X] [-Date YYYY-MM-DD]  Show sports schedule by sport & date"
        Write-Host ""
        Write-Host "Schedule sport keywords:" -ForegroundColor Yellow
        Write-Host "  nba, nfl, mlb, nhl, soccer/epl, atp/tennis, ufc/mma, cs2, lol, f1, pga/golf, boxing"
    }
}
