# EDA Code Patterns

Use these snippets inside `mcp__easyeda__execute_in_eda`.

## Inspect State

```javascript
const project = await eda.dmt_Project.getCurrentProjectInfo();
const page = await eda.dmt_Schematic.getCurrentSchematicPageInfo();
return { project: project?.friendlyName, page: page?.name };
```

## Create A Schematic Page

```javascript
const page = await eda.dmt_Schematic.getCurrentSchematicPageInfo();
const uuid = await eda.dmt_Schematic.createSchematicPage(page.parentSchematicUuid);
await eda.dmt_Schematic.modifySchematicPageName(uuid, "Circuit");
await eda.dmt_EditorControl.openDocument(uuid);
return { uuid };
```

## Place Real Parts And Read Pins

```javascript
async function findDevice(query, exact) {
  const list = await eda.lib_Device.search(query, undefined, undefined, undefined, 12, 1);
  return list.find(x => x.name === exact) || list[0];
}

function pinInfo(p) {
  return {
    id: p?.getState_PrimitiveId?.(),
    name: p?.getState_PinName?.(),
    number: p?.getState_PinNumber?.(),
    x: p?.getState_X?.(),
    y: p?.getState_Y?.(),
    rotation: p?.getState_Rotation?.()
  };
}

async function place(query, exact, x, y, rotation = 0) {
  const dev = await findDevice(query, exact);
  if (!dev) throw new Error(`Device not found: ${query}`);
  const comp = await eda.sch_PrimitiveComponent.create(dev, x, y, undefined, rotation, false, true, true);
  const id = comp?.getState_PrimitiveId?.();
  const pins = id ? await eda.sch_PrimitiveComponent.getAllPinsByPrimitiveId(id) : [];
  return { dev, comp, id, pins: (pins || []).map(pinInfo) };
}
```

## Create Readable Net Stubs

```javascript
async function netStub(x, y, direction, net) {
  const len = 28;
  const line =
    direction === "L" ? [x, y, x - len, y] :
    direction === "R" ? [x, y, x + len, y] :
    direction === "U" ? [x, y, x, y - len] :
    [x, y, x, y + len];
  await eda.sch_PrimitiveWire.create(line, net);
  await eda.sch_PrimitiveText.create(line[2] + 4, line[3] - 4, net, 0, null, null, 8, true);
}
```

## Validate Recent Wires

```javascript
const wires = await eda.sch_PrimitiveWire.getAll();
return wires.slice(-30).map(w => ({
  id: w.getState_PrimitiveId?.(),
  net: w.getState_Net?.(),
  line: w.getState_Line?.()
}));
```
