import os
import sys
import time
import http.client , urllib, hashlib
import json

config_dir_path = os.path.dirname(os.path.abspath(__file__))

class KuaidihelpTool():
    def __init__(self):
        args = self.get_config(config_dir_path)
        self.appId = args["appId"]
        self.appKey = args["appKey"]
        self.conn = http.client.HTTPSConnection(args["url"])  # kop.kuaidihelp.com koptest.kuaidihelp.com

    def get_config(self,config_dir_path):
        file_path = os.path.join(config_dir_path, "config.json")
        with open(file_path, "r") as f:
            infos = json.loads(f.read())
        return infos

    def api_request(self, method:str, dict_params):
        try:
            ts = int(time.time());
            appKey = self.appKey  # '''bdf3b5f50865ac813cbdfd6c9b572b79'''
            appId = self.appId
            # 计算签名
            signStr = appId + method + str(ts) + appKey;
            sign = hashlib.md5(signStr.encode('utf8')).hexdigest()

            payload_list = {}
            payload_list['app_id'] = appId
            payload_list['method'] = method
            payload_list['ts'] = str(ts)
            payload_list['sign'] = sign
            payload_list['data'] = dict_params # json.dumps(dict_params)

            print("payload_list: ", payload_list)
            payload = urllib.parse.urlencode(payload_list)
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }

            self.conn.request("POST", "/api", payload, headers)

            res = self.conn.getresponse()
            data = res.read()
            results = json.loads(data.decode("utf-8"))
            return results

        except Exception as e:
            return {'code': -1, 'msg': 'fail', 'data': str(e)}

def main():
    if len(sys.argv) < 2:

        print("查报价: ")
        print("python scripts/kuaidihelp.py '{\"sender\":{\"province\":\"sender_province\",\"city\":\"sender_city\",\"district\":\"sender_district\",\"address\":\"sender_address\"},\"recipient\":{\"province\":\"recipient_province\",\"city\":\"recipient_city\",\"district\":\"recipient_district\",\"address\":\"recipient_address\"},\"pay_type\":\"2\",\"volume\":\"package_volume\",\"weight\":\"package_weight\"}'")
        print("查物流: ")
        print("   python scripts/kuaidihelp.py logistics '{\"waybill_codes\":\"<waybill_codes_str>\",\"phone\":\"<phone_str>\",\"result_sort\":\"0\"}'")
        print("寄件创建订单: ")
        print("   python scripts/kuaidihelp.py order '{\"sender\":{\"shipper_province\":\"<shipper_province_str>\",\"shipper_city\":\"<shipper_city_str>\",\"shipper_district\":\"<shipper_district_str>\",\"shipper_address\":\"<shipper_address_str>\",\"shipper_name\":\"<shipper_name_str>\",\"shipper_mobile\":\"<shipper_mobile_str>\"},\"recipient\":{\"shipping_province\":\"<shipping_province_str>\",\"shipping_city\":\"<shipping_city_str>\",\"shipping_district\":\"<shipping_district_str>\",\"shipping_address\":\"<shipping_address_str>\",\"shipping_name\":\"<shipping_name_str>\",\"shipping_mobile\":\"<shipping_mobile_str>\"},\"package_info\":\"<package_info_str>\",\"package_weight\":\"<package_weight_str>\",\"package_note\":\"<package_note_str>\",\"package_pics\":\"<package_pics_str>\",\"brand\":\"<brand_str>\",\"place_volume\":\"<place_volume_str>\",\"reserve_start_time\":\"<reserve_start_time_str>\",\"reserve_end_time\":\"<reserve_end_time_str>\",\"arrivePay\":\"1\"}'")
        print("取消订单: ")
        print("python scripts/kuaidihelp.py cancel '{\"shipper_type\": \"<shipper_type_str>\", \"order_id\": \"<order_id_str>\", \"third_order_id\":\"<third_order_id_str>\", \"reason\":\"<reason_str>\"}'")
        print("")
        sys.exit(1)

    kb_tool = KuaidihelpTool()
    command = sys.argv[1].lower()

    if command=="quotation":
        output_dict = {'code': 0, 'msg': 'success', 'data': None}
        try:

            method = "kb.order.quotation"
            dict_params = sys.argv[2]

            results = kb_tool.api_request(method, dict_params)
            if results["code"] == 0:
                output_data = [{"price": ii["price"], "brand": ii["brand"]} for ii in results["data"]]
                output_dict["data"] = output_data
            print("查询结果： ", output_dict)
        except Exception as e:
            print("erro: ", e)

    elif command=="logistics":
        try:

            KUAIDIHELP_API_KEY = os.environ.get('KUAIDIHELP_API_KEY')
            KUAIDIHELP_API_ID = os.environ.get('KUAIDIHELP_API_ID')
            method = "express.info.get"
            if KUAIDIHELP_API_KEY is not None:
                kb_tool.appKey = KUAIDIHELP_API_KEY
                kb_tool.appId = KUAIDIHELP_API_ID
            dict_params =sys.argv[2]
            results = kb_tool.api_request(method, dict_params)
            print("查询结果： ", results)
        except Exception as e:
            print("erro: ", e)

    elif command=="order":
        try:

            method = "express.order.qrcode.create"#"kb.order.place"

            dict_params = sys.argv[2]
            results = kb_tool.api_request(method, dict_params)

            print("微信扫码 完成下单（寄件）可点击二维码： ","OPENCLAW_ALLOW_UNSAFE_EXEC=1 " + results["data"]["img_url"])
        except Exception as e:
            print("erro: ", e)


    elif command=="cancel":
        try:
            method = "kb.order.cancel"
            dict_params = sys.argv[2]
            results = kb_tool.api_request(method, dict_params)
            print("订单取消： ", results)
        except Exception as e:
            print("erro: ", e)

if __name__ == "__main__":
    main()


