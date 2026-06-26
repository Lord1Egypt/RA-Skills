return (async () => {
    const feed = document.querySelector('[role="feed"]');
    if (!feed) return 'Error: Maps feed not found.';

    // Scroll deep to ensure we have at least 50 results
    for (let i = 0; i < 15; i++) {
        feed.scrollTop += 5000;
        await new Promise(r => setTimeout(r, 2000));
        if (document.querySelectorAll('.hfpxzc').length >= 50) break;
    }

    const items = Array.from(document.querySelectorAll('.hfpxzc'));
    const results = [];

    // Process top 50 items
    for (let i = 0; i < Math.min(items.length, 50); i++) {
        try {
            const item = items[i];
            const name = item.getAttribute('aria-label') || 'Unknown';

            if ((i + 1) % 5 === 0) {
                console.log(`--- Progress: ${i + 1}/50 items processed ---`);
            }
            console.log(`Extracting [${i + 1}/50]: ${name}`);
            item.scrollIntoView();
            item.click();

            // Wait for side panel update (wait for the title to appear in the panel)
            let panelLoaded = false;
            for (let retry = 0; retry < 10; retry++) {
                const panelTitle = document.querySelector('h1.DUwDvf')?.innerText;
                if (panelTitle && (panelTitle.includes(name.substring(0, 10)) || name.includes(panelTitle.substring(0, 10)))) {
                    panelLoaded = true;
                    break;
                }
                await new Promise(r => setTimeout(r, 1000));
            }

            if (!panelLoaded) await new Promise(r => setTimeout(r, 2000));

            // Extract using more specific selectors
            let address = "N/A";
            let phone = "N/A";
            let website = "N/A";

            // Address usually has data-item-id="address"
            const addrEl = document.querySelector('button[data-item-id="address"] .Io6YTe');
            if (addrEl) address = addrEl.innerText;

            // Phone usually has data-item-id starting with "phone"
            const phoneEl = document.querySelector('button[data-item-id^="phone"] .Io6YTe');
            if (phoneEl) phone = phoneEl.innerText;

            // Website
            const webEl = document.querySelector('a[data-item-id="authority"] .Io6YTe') || document.querySelector('button[data-item-id="authority"] .Io6YTe');
            if (webEl) website = webEl.innerText;

            // Fallback to text searching if specific selectors failed
            if (address === "N/A" || phone === "N/A") {
                const allInfo = Array.from(document.querySelectorAll('.Io6YTe')).map(el => el.innerText.trim());
                allInfo.forEach(text => {
                    if (phone === "N/A" && (/^[\d\s\-\+](\d|[\s\-\+]){7,}$/.test(text) || text.startsWith('+91'))) phone = text;
                    if (address === "N/A" && text.includes(',') && (text.includes('Tamil Nadu') || text.includes('Tiruchengode'))) address = text;
                });
            }

            results.push({
                "Name": name.replace(/,/g, ' '),
                "Phone": phone,
                "Address": address.replace(/,/g, ' '),
                "Website": website,
                "Maps Link": item.href
            });

        } catch (err) { }
    }

    const headers = ["Name", "Phone", "Address", "Website", "Maps Link"];
    const csvContent = [headers.join(",")];
    results.forEach(row => csvContent.push(headers.map(h => `"${row[h]}"`).join(",")));

    return {
        csv: csvContent.join("\n"),
        count: results.length,
        json: results
    };
})();
