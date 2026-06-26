const express = require('express');
const { getMbusaDealers, getMbusaInventory, getMbusaUsedInventory } = require('./src/tool.js'); 

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

// ==========================================
// ENDPOINT: Dealer Locator
// ==========================================
app.get('/api/dealers', async (req, res) => {
    try {
        const zip = req.query.zip;
        if (!zip) return res.status(400).json({ status: "error", message: "Missing required parameter: zip" });

        const start = req.query.start ? parseInt(req.query.start, 10) : 0;
        const count = req.query.count ? parseInt(req.query.count, 10) : 10;
        const filter = req.query.filter || "mbdealer";

        const resultString = await getMbusaDealers(zip, start, count, filter);
        const resultJson = JSON.parse(resultString);
        if (resultJson.status === "error") return res.status(502).json(resultJson); 

        res.status(200).json(resultJson);
    } catch (error) {
        console.error("Dealer API Error:", error);
        res.status(500).json({ status: "error", message: "Internal server error" });
    }
});

// ==========================================
// ENDPOINT: NEW Vehicle Inventory Search
// ==========================================
app.get('/api/inventory', async (req, res) => {
    try {
        if (!req.query.zip) return res.status(400).json({ status: "error", message: "Missing required parameter: zip" });

        const params = {
            zip: req.query.zip,
            dealerId: req.query.dealerId,
            model: req.query.model,
            classId: req.query.classId,
            bodyStyle: req.query.bodyStyle,
            brand: req.query.brand,
            exteriorColor: req.query.exteriorColor,
            interiorColor: req.query.interiorColor,
            highwayFuelEconomy: req.query.highwayFuelEconomy,
            fuelType: req.query.fuelType,
            distance: req.query.distance ? parseInt(req.query.distance, 10) : undefined,
            minPrice: req.query.minPrice ? parseInt(req.query.minPrice, 10) : undefined,
            maxPrice: req.query.maxPrice ? parseInt(req.query.maxPrice, 10) : undefined,
            minYear: req.query.minYear ? parseInt(req.query.minYear, 10) : undefined,
            maxYear: req.query.maxYear ? parseInt(req.query.maxYear, 10) : undefined,
            passengerCapacity: req.query.passengerCapacity ? parseInt(req.query.passengerCapacity, 10) : undefined,
            year: req.query.year ? parseInt(req.query.year, 10) : undefined,
            start: req.query.start ? parseInt(req.query.start, 10) : 0,
            count: req.query.count ? parseInt(req.query.count, 10) : 12
        };

        const resultString = await getMbusaInventory(params);
        const resultJson = JSON.parse(resultString);
        if (resultJson.status === "error") return res.status(502).json(resultJson); 

        res.status(200).json(resultJson);
    } catch (error) {
        console.error("New Inventory API Error:", error);
        res.status(500).json({ status: "error", message: "Internal server error" });
    }
});

// ==========================================
// ENDPOINT: USED/CPO Vehicle Inventory Search
// ==========================================
app.get('/api/used-inventory', async (req, res) => {
    try {
        if (!req.query.zip) return res.status(400).json({ status: "error", message: "Missing required parameter: zip" });
        if (!req.query.invType) return res.status(400).json({ status: "error", message: "Missing required parameter: invType (cpo or pre)" });

        const params = {
            zip: req.query.zip,
            invType: req.query.invType,
            dealerId: req.query.dealerId,
            model: req.query.model,
            classId: req.query.classId,
            bodyStyle: req.query.bodyStyle,
            brand: req.query.brand,
            exteriorColor: req.query.exteriorColor,
            interiorColor: req.query.interiorColor,
            highwayFuelEconomy: req.query.highwayFuelEconomy,
            fuelType: req.query.fuelType,
            mileage: req.query.mileage,
            distance: req.query.distance ? parseInt(req.query.distance, 10) : undefined,
            minPrice: req.query.minPrice ? parseInt(req.query.minPrice, 10) : undefined,
            maxPrice: req.query.maxPrice ? parseInt(req.query.maxPrice, 10) : undefined,
            minYear: req.query.minYear ? parseInt(req.query.minYear, 10) : undefined,
            maxYear: req.query.maxYear ? parseInt(req.query.maxYear, 10) : undefined,
            passengerCapacity: req.query.passengerCapacity ? parseInt(req.query.passengerCapacity, 10) : undefined,
            year: req.query.year ? parseInt(req.query.year, 10) : undefined,
            start: req.query.start ? parseInt(req.query.start, 10) : 0,
            count: req.query.count ? parseInt(req.query.count, 10) : 12
        };

        const resultString = await getMbusaUsedInventory(params);
        const resultJson = JSON.parse(resultString);
        if (resultJson.status === "error") return res.status(502).json(resultJson); 

        res.status(200).json(resultJson);
    } catch (error) {
        console.error("Used Inventory API Error:", error);
        res.status(500).json({ status: "error", message: "Internal server error" });
    }
});

app.listen(PORT, () => {
    console.log(`🚀 MBUSA Skill API is running on port ${PORT}`);
    console.log(`Test Dealers: http://localhost:${PORT}/api/dealers?zip=10019`);
    console.log(`Test New Inventory: http://localhost:${PORT}/api/inventory?zip=10019&distance=50`);
    console.log(`Test Used Inventory: http://localhost:${PORT}/api/used-inventory?zip=10019&invType=cpo`);
});