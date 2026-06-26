using System;
using UnityEngine;

[Serializable]
public class GotchiRenderWearables
{
    public int body = 0;
    public int face = 0;
    public int eyes = 0;
    public int head = 0;
    public int pet = 0;
    public int hand_left = 0;
    public int hand_right = 0;
}

[Serializable]
public class GotchiRenderOutput
{
    public string slug = "custom-gotchi";
    public string full_png = "Renders/custom-gotchi-full.png";
    public string headshot_png = "Renders/custom-gotchi-headshot.png";
    public string manifest_json = "Renders/custom-gotchi-manifest.json";
}

[Serializable]
public class GotchiRenderRequest
{
    public int haunt_id = 1;
    public string collateral = "ETH";
    public string eye_shape = "Mythical";
    public string eye_color = "High";
    public int skin_id = 0;
    public string background = "transparent";
    public string pose = "idle";
    public GotchiRenderWearables wearables = new GotchiRenderWearables();
    public GotchiRenderOutput output = new GotchiRenderOutput();
}

[Serializable]
public class GotchiRenderResult
{
    public bool ok;
    public string status;
    public string message;
    public string full_png;
    public string headshot_png;
    public string manifest_json;
    public string unity_version;
    public GotchiRenderRequest request;
}
