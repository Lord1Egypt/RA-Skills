//消息发送组件
export default{
data() {return {
    dlg:false,
    batch:[], //按设备号批量发送
    msg:'',
    tmpls:[],
    tmpl:'',
    percent:{val:0,each:0},
    type:"1", //1：按客户，2：按设备
    errMsg:'',
    customer:0,
}},
props: {
    title:{type:String,required:true},
    custId:{type:Number, required:true}, //客户ID
    custName:{type:String, required:true},
    service:{type:String, required:true},
    batchNum:{type:Number, required:false, default:150},
    tags:{type:Object, required:false, default:{}}
},
created() {
    this.getTmpls();
    request({method:"GET",url:"/admin/customer"}, this.service).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.errMsg=this.tags.failed + resp.code + ',' + resp.info;
            return;
        }
        this.customer=resp.data.customer;
    });
},
methods:{
show() {
    this.dlg=true;
    this.errMsg='';
},
sendMessage() {
    if(this.type==1) {
        this.send_by_customer(this.custId, this.msg);
    } else if(this.type==2) {
        var codes=this.batch.split(/[(\r\n)\r\n;]+/);
        this.percent.val=0;
        if(codes.length<this.batchNum) {
            this.percent.each=0;//不显示
        } else {
            var n=Math.ceil(codes.length/this.batchNum);
            this.percent.each=1.0/n;
        }
        this.send_by_codes(codes,this.msg,0);
    } else {
        var msgs=this.batch.split(/[(\r\n)\r\n]+/);
        this.percent.val=0;
        if(msgs.length<this.batchNum*2) {
            this.percent.each=0;//不显示
        } else {
            var n=Math.ceil(msgs.length/(this.batchNum*2));
            this.percent.each=1.0/n;
        }
        this.send_by_msgs(msgs,0);
    }
},
send_by_customer(customer, msg) {
    var url=this.customer>0?"/msg/send_by_customer":"/msg/pro_send_by_customer";
    var dta={customer:customer,msg:msg,maxTimes:1};
    request({method:"POST",url:url,data:dta}, this.service).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.errMsg=this.tags.failed + resp.code + ',' + resp.info;
            return;
        }
        this.errMsg='';
        this.dlg=false;
    });
},
send_by_codes(codes,msg,start) {
    var dta={msg:msg,codes:[],maxTimes:1};
    for(var n=0,i=start,l=codes.length; i<l&&n<this.batchNum; i++,n++) {
        dta.codes.push(codes[i]);
    }
    var url=this.customer>0?"/msg/send_by_codes":"/msg/pro_send_by_codes";
    request({method:"POST",url:url,data:dta}, this.service).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.errMsg=this.tags.failed + resp.code + ',' + resp.info;
            this.percent.val=0;
            return;
        }
        
        this.percent.val+=this.percent.each;
        if(start+this.batchNum < codes.length) {
            this.send_by_codes(codes,msg,start+this.batchNum);
            return;
        }
        this.dlg=false;
    }); 
},
send_by_msgs(msgs,start) {
    var dta={msgs:[],maxTimes:1};
    for(var n=0,i=start,l=msgs.length; i<l&&n<this.batchNum; i+=2,n++) {
        dta.msgs.push({code:msgs[i], msg:msgs[i+1]});
    }
    var url=this.customer>0?"/msg/send_by_msgs":"/msg/pro_send_by_msgs";
    request({method:"POST",url:url, data:dta}, this.service).then(resp =>{
        if(resp.code!=RetCode.OK) {
            this.errMsg=this.tags.failed + resp.code + ',' + resp.info;
            this.percent.val=0;
            return;
        }
        
        this.percent.val+=this.percent.each;
        if(start+this.batchNum*2 < msgs.length) {
            this.send_by_msgs(msgs,start+this.batchNum*2);
            return;
        }
        this.dlg=false;
    }); 
},
getTmpls() {
    var url="/api/msgtpl/list";
    request({method:"GET",url:url}, this.service).then(resp=>{
        if(resp.code!=RetCode.OK || !('data' in resp) || !('tpls' in resp.data)) {
            Console.info("request templates failed:" + resp.code + ",info:" + resp.info);
            this.tmpls=[];
        } else {
            var opts=[];
            for(var t of resp.data.tpls) {
                opts.push({label:t.name,value:t.tpl});
            }
            this.tmpls=opts;
        }
    });
}
},
computed: {
   value: {
      get() {return this.modelValue},
      set(v) {this.$emit('update:modelValue', v)}
   }
},
template: `
<q-dialog v-model="dlg" no-backdrop-dismiss>
  <q-card style="min-width:75vw">
    <q-linear-progress :value="percent.val" color="pink" v-show="percent.val>0"></q-linear-progress>
    <q-card-section>
     <div class="text-h6">{{title}} {{custName}}</div>
    </q-card-section>
    <q-card-section class="q-pt-none">
    <div class="q-gutter-sm">
     <q-radio v-model="type" :label="tags.byCust" val="1"></q-radio>
     <q-radio v-model="type" :label="tags.byCodes" val="2"></q-radio>
     <q-radio v-model="type" :label="tags.byMsgs" val="3"></q-radio>
    </div>
    <q-list v-show="type<3">
      <q-item><q-item-section>
       <q-select emit-value map-options :options="tmpls" dense
       @update:model-value="(v)=>{msg=v}" v-model="tmpl"></q-select>
      </q-item-section></q-item>
      <q-item><q-item-section>
       <q-input v-model="msg" :label="tags.message" dense maxlength=300></q-input>
      </q-item-section></q-item>
      <q-item v-show="type==2"><q-item-section>
       {{tags.codePrompt}}<br><span class="text-red">{{tags.codeFmt}}</span>
       <q-input v-model="batch" :label="tags.code"
        dense maxlength=100000 type="textarea" rows="12"></q-input>
      </q-item-section></q-item>
    </q-list>
    <q-list v-show="type==3">
      <q-item><q-item-section>
       {{tags.msgPrompt}}<br><span class="text-red">{{tags.msgFmt}}</span>
       <q-input v-model="batch" :label="tags.message"
        dense maxlength=100000 type="textarea" rows="12"></q-input>
      </q-item-section></q-item>
    </q-list>
    </q-card-section>
    <q-card-section>
     <div class="text-red" v-if="errMsg!=''">{{errMsg}}</div>
    </q-card-section>
    <q-card-actions align="right">
      <q-btn :label="tags.confirm" color="primary" @click.stop="sendMessage"></q-btn>
      <q-btn flat :label="tags.close" color="primary" v-close-popup></q-btn>
    </q-card-actions>
  </q-card>
</q-dialog>
`}