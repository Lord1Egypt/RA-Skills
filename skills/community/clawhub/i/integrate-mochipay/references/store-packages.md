# Current store packages — WEB82.102

Hashes below pin the local WEB82.102 release. Verify a downloaded archive before installation; hosted deployment may lag the prepared release.

## WooCommerce
https://mochi.bz/Downloads/MochiPay_WooCommerce_1.5.24_Multilanguages.zip
SHA256: `4c0423b6e3c861d232c18ec9c7176bce8b7f9cbafc09969112545699ff6683c3`

## OpenCart 2.0–2.2
https://mochi.bz/Downloads/MochiPay_OpenCart_2.0-2.2_Multilanguages.ocmod.zip
SHA256: `a6e26d2b2c04acb028eef736a9ecfa44ac091a6520413bd4f61e3adffb88d503`

## OpenCart 2.3
https://mochi.bz/Downloads/MochiPay_OpenCart_2.3_Multilanguages.ocmod.zip
SHA256: `11dfd6a626f6f0995e2b8830695890d8ae2eb245ac328921846bf6fff9262a07`

## OpenCart 3
https://mochi.bz/Downloads/MochiPay_OpenCart_3_Multilanguages.ocmod.zip
SHA256: `e6ebe60bb66378b5fbd6208bc564fd8bf136dae8dc9ffd1a08374d40163c3434`

## OpenCart 4
https://mochi.bz/Downloads/OpenCart4/mochipay-multilanguages.ocmod.zip
SHA256: `ebccaedddb6124d091e92dba022d9b4d8a4b5890dde6ce46570b4d3b68415a1f`

## Zen Cart 1.5.3–1.5.7
https://mochi.bz/Downloads/MochiPay_ZenCart_1.5.3-1.5.7_Multilanguages.zip
SHA256: `25089ca50f8097c69333179c64fd3a091c89a922577a1687cbbc4f12401accf0`

## Zen Cart 1.5.8–2.2
https://mochi.bz/Downloads/MochiPay_ZenCart_1.5.8-2.2_Multilanguages.zip
SHA256: `58db4fb8bdad7328169b62218f34a506fab1e405aac1a5577b387a6a6a84bf06`

## Magento 1 / OpenMage
https://mochi.bz/Downloads/MochiPay_Magento1_OpenMage_Multilanguages.zip
SHA256: `fc7efadb9dc3d206d7a89508882ca68ff1ff0130e42c050fdad1fd01e912825e`

## Magento 2
https://mochi.bz/Downloads/MochiPay_Magento2_Multilanguages.zip
SHA256: `d0ae0b91b4b68252bb0cbfef8953499b882a6aa3377d42aaff08522171afe23e`

## PrestaShop 1.6
https://mochi.bz/Downloads/MochiPay_PrestaShop_1.6_Multilanguages.zip
SHA256: `bbddbad719214b83af5e52c1dd7bc00c04645156864cf04a9b92f25fdedb967e`

## PrestaShop 1.7 / 8 / 9
https://mochi.bz/Downloads/MochiPay_PrestaShop_1.7-9_Multilanguages.zip
SHA256: `25f6b675fb06bcb5a851f0b97caf1aacdb602aa8941e6a6a68cf1321ebad42a4`

## Shopware 6.6
https://mochi.bz/Downloads/MochiPay_Shopware_6.6_1.0.11_Multilanguages.zip
SHA256: `fdd5caee55d4a6343b47023add39f43ce94f0349d37f3eaff42072fd614adf68`

## Shopware 6.7
https://mochi.bz/Downloads/MochiPay_Shopware_6.7_1.0.11_Multilanguages.zip
SHA256: `a9dcc9ab73f12da98d3d1b70d3284b0c385fef2f441945c798a82849f6effae4`

## Drupal Commerce
https://mochi.bz/Downloads/MochiPay_Drupal_Commerce_1.0.11_Multilanguages.zip
SHA256: `0a3d5887d66c4f8c96908ea36c41909463fcf31f4bca963f205f2c21fcebeb12`

## EC-CUBE 4.3
https://mochi.bz/Downloads/MochiPay_EC-CUBE_4.3_1.0.11_Multilanguages.zip
SHA256: `40dece1a8d56b17c45a9507d1bdc62a7c73ac77baec00b6e7d5b1f72838776b4`

## Bagisto 2.3
https://mochi.bz/Downloads/MochiPay_Bagisto_2.3_1.0.11_Multilanguages.zip
SHA256: `f5c6462128b86ff665fc778926d92df3b09f5642daea8c775f5bd952c1777ad2`

## Sylius 2.0
https://mochi.bz/Downloads/MochiPay_Sylius_2.0_1.0.11_Multilanguages.zip
SHA256: `4dfc454eae892e9528e8feb59b03d779d04cfed70667e8e218a27175d8180c6d`

## osCommerce 4.14
https://mochi.bz/Downloads/MochiPay_osCommerce_4.14_1.0.11_Multilanguages.zip
SHA256: `18fe7823c7a51af98136bfff15e2dcc2372d27bf3de98736f546763255dde4ed`

## thirty bees 1.6
https://mochi.bz/Downloads/MochiPay_thirty_bees_1.6_1.0.11_Multilanguages.zip
SHA256: `3b3f17422fcf1ad62a025d2dbab7125549534cb62a3286ff64a3eaa5d27ef3a0`

## Classic SaaS — two HPP integration modes

Shopyy/Shopoem, Shoplus, Wooshoppaas and Fecify use HPP without a native plugin.

### 1. Fixed coin and network

POST `https://mochi.bz/api/v/orders/legacy_create/YOUR_API_KEY/USDT_TRC20`

Replace the final segment with a supported payment method. The customer opens that method's payment instructions directly.

### 2. Customer chooses on the hosted checkout

POST `https://mochi.bz/api/v/orders/legacy_create/YOUR_API_KEY`

Omit the method segment. The customer chooses an available coin/network on HPP. Once the payment instructions and QR code are generated, that method is locked for this order.

Both modes keep the existing POST parameters, response format, return flow and notification flow. The URL contains the API key, never the API secret. Keep the same request ID when retrying an unchanged creation request.

Guides: https://mochi.bz/Guides/GuideShopyy.aspx (also Shopoem), https://mochi.bz/Guides/GuideShoplus.aspx, https://mochi.bz/Guides/GuideWooshoppaas.aspx and https://mochi.bz/Guides/GuideFecify.aspx.
